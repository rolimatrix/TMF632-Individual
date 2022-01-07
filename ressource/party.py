# coding=utf-8
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flasgger.utils import swag_from
from marshmallow import ValidationError, EXCLUDE

from model.individual import Individual
from model.characteristic import Characterstic
from model.contact_medium import ContactMedium
from model.relatedparty import RelatedParty
from schemas.Individual import IndividualSchema, IndivtoTMF
from schemas.medium import MediumSchema
from schemas.characteristic import CharacteristicSchema
from schemas.relatedParty import RelatedPartySchema
from tmf_errors import errorFormaterMarshmallow
import os
from conf import _init_logging
from iteration_utilities import unique_everseen, duplicates

from extensions import db

#get global Fehlerbildnummer Prefix as Env Variable
FBNRPREFIX = os.environ.get('FBNRPREFIX', '99999999')

#init logging
logger= _init_logging('ressource.party')

Individual_Schema = IndividualSchema()
IndivTMF632_Schema= IndivtoTMF()
Medium_Schema = MediumSchema()
Characteristic_Schema = CharacteristicSchema()
RelatedParty_Schema = RelatedPartySchema()

def isValidJSON(func):
  def wrapper(*args, **kwargs):
    try:
      json_data = request.get_json()
      return func(*args, **kwargs)

    except:
      FNummer = FBNRPREFIX + '00000005'
      logger.error("http code 400, Invalid not well formed Json",
                  extra={'fehlerbildnummer': FNummer, 'incomming_message': "",
                          'communication_pattern': 'req-reply', 'service_domain': 'party',
                          'service_call': request.url})
      return errorFormaterMarshmallow(400, 'Json Validation errors', None, 'Invalid not well formed Json', 'Technical Error', FNummer), HTTPStatus.BAD_REQUEST
  return wrapper

def load_json(json_data):
    output_dict = {}
    for key, value in json_data.items():
        if not type(value) == list:
            if type(value) == dict:
                for keyD, valueD in value.items():
                    if type(valueD)== str:
                        k=keyD.replace("@", "")
                        if valueD!='null':
                            output_dict[k] = valueD
            elif type(value)== str or type(value)== bool or value is None:
                k=key.replace("@", "")
                output_dict[k] = value

    return output_dict


class Party(Resource):

    @swag_from('TMF632PartyIndiv_V1.yaml',endpoint='individual', methods=['POST'])
    @isValidJSON
    def post(self):
        json_data = request.get_json()
        #pick up all different root Elements from requested Json
        indivJson= catch_Json(json_data, 'root')
        mediumJson = catch_Json(json_data, 'medium')
        CharJson = catch_Json(json_data, 'character')
        relPartyJson = catch_Json(json_data, 'relparty')

        # check Json for Individual, Medium, character and relatedParty with Marshmallow Schema
        try:
            data = Individual_Schema.load(data=indivJson)
        except ValidationError as errors:
            FNummer = FBNRPREFIX + '00000004'
            logger.error(errorFormaterMarshmallow(400, 'Validation errors', errors),
                         extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                'communication_pattern': 'req-reply', 'service_domain': 'party',
                                'service_call': request.url})
            return errorFormaterMarshmallow(400, 'Validation errors', errors,
                                            'mandatory Values for Individual Json not delivered', 'Business Error',
                                            FNummer), HTTPStatus.BAD_REQUEST

        if mediumJson:
            # it could be that we have more then one medium
            for m in mediumJson:
                # Make Contact Medium flat (without dictionary characterstic and validFor)
                medium = load_json(m)
                try:
                    dataM = Medium_Schema.load(data=medium)
                except ValidationError as errors:
                    FNummer = FBNRPREFIX + '00000006'
                    logger.error(errorFormaterMarshmallow(400, 'Validation errors', errors),
                                 extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                        'communication_pattern': 'req-reply', 'service_domain': 'party',
                                        'service_call': request.url})
                    return errorFormaterMarshmallow(400, 'Validation errors', errors,
                                                    'validation for medium with error', 'Business Error',
                                                    FNummer), HTTPStatus.BAD_REQUEST
        if CharJson:
            try:
                dataM = CharacteristicSchema(many=True).load(data=CharJson)
            except ValidationError as errors:
                FNummer = FBNRPREFIX + '00000007'
                logger.info(errorFormaterMarshmallow(400, 'Validation errors', errors),
                            extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                   'communication_pattern': 'req-reply', 'service_domain': 'party',
                                   'service_call': request.url})
                return errorFormaterMarshmallow(400, 'Validation errors', errors,
                                                'validation for party Character with error', 'Business Error',
                                                FNummer), HTTPStatus.BAD_REQUEST
        if relPartyJson:
            try:
                dataM = RelatedPartySchema(many=True).load(data=relPartyJson)
            except ValidationError as errors:
                FNummer = FBNRPREFIX + '00000008'
                logger.info(errorFormaterMarshmallow(400, 'Validation errors', errors),
                            extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                   'communication_pattern': 'req-reply', 'service_domain': 'party',
                                   'service_call': request.url})
                return errorFormaterMarshmallow(400, 'Validation errors', errors,
                                                'validation for related party Character with error', 'Business Error',
                                                FNummer), HTTPStatus.BAD_REQUEST
        ### end Marshmallow Check. Now we know that request delivered JSON that matches to Swagger Spec

        #now check if Business Key for medium, relatedParty and Character are unique
        if mediumJson and checkUniqueBusinessID(mediumJson, 'medium',method="post") is True:
            FNummer = FBNRPREFIX + '00000001'
            logger.error("http code 400, Business Key violation at contactMedium",
                         extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                'communication_pattern': 'req-reply', 'service_domain': 'party',
                                'service_call': request.url})
            return errorFormaterMarshmallow(400, 'Business Key violation at contactMedium', None, 'mediumType for contactMedium can only exist once per each party',
                                            'Business Error', FNummer), HTTPStatus.BAD_REQUEST
        if relPartyJson and checkUniqueBusinessID(relPartyJson, 'relatedParty',method="post") is True:
            FNummer = FBNRPREFIX + '00000002'
            logger.error("http code 400, Business Key violation at relatedParty",
                         extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                'communication_pattern': 'req-reply', 'service_domain': 'party',
                                'service_call': request.url})
            return errorFormaterMarshmallow(400, 'Business Key violation at relatedParty', None, 'id for Related Party can only exist once per each party and must have valid Value',
                                            'Business Error', FNummer), HTTPStatus.BAD_REQUEST
        if CharJson and checkUniqueBusinessID(CharJson, 'partyCharacteristic',method="post") is True:
            FNummer = FBNRPREFIX + '00000003'
            logger.error("http code 400, Business Key violation at partyCharResacteristic",
                         extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                'communication_pattern': 'req-reply', 'service_domain': 'party',
                                'service_call': request.url})
            return errorFormaterMarshmallow(400, 'Business Key violation at partyCharResacteristic', None, 'name for partyCharResacteristic can only exist once per each party',
                                            'Business Error', FNummer), HTTPStatus.BAD_REQUEST
        ### now we know that there is no Business Key violation

        # now start Session Contex sequentiell
        partyIndiv = Individual(**data)
        db.session.add(partyIndiv)
        if mediumJson:
            for m in mediumJson:
                # Make Contact Medium flat (without dictionary Characterstic and valid)
                medium = load_json(m)
                dataM = Medium_Schema.load(data=medium)
                contactMediumRes = ContactMedium(dataM,partyIndiv)
                db.session.add(contactMediumRes)
        if CharJson:
            # it could be that we have more then one characteristic
            for ch in CharJson:
                character = load_json(ch)
                dataM = Characteristic_Schema.load(data=character)
                partyCharRes = Characterstic(dataM,partyIndiv)
                db.session.add(partyCharRes)
        if relPartyJson:
            # it could be that there are more then one relParty existent
            for rel in relPartyJson:
                rel= load_json(rel)
                dataM = RelatedParty_Schema.load(data=rel)
                relPartyRes= RelatedParty(dataM,partyIndiv)
                db.session.add(relPartyRes)
        #### ORM Session Context finished
        db.session.commit()
        partyIndiv = Individual.get_by_id(partyIndiv.id)
        logger.info("Party with ID {} created".format(partyIndiv.id),extra={'fehlerbildnummer': "", 'incomming_message': json_data,
                                        'communication_pattern': 'req-reply', 'service_domain': 'party',
                                        'service_call': request.url})
        return IndivTMF632_Schema.dump(partyIndiv), HTTPStatus.OK

class PartyId(Resource):
    @swag_from('TMF632PartyIndiv_V1.yaml', endpoint='/individual/{id}', methods=['DELETE'])
    def delete(self, id):
        partyIndiv = Individual.get_by_id(indiv_id=id)

        if partyIndiv is None:
            FNummer = FBNRPREFIX + '00000009'
            logger.warning(errorFormaterMarshmallow(400,'On delete EP',None,"Party ID {} not exsiting".format(id)),
                           extra={'fehlerbildnummer': FNummer,'incomming_message': id,
                                       'communication_pattern': 'req-reply', 'service_domain': 'party', 'service_call':request.url})
            return errorFormaterMarshmallow(400,'On delete EP',None,"Party ID {} not existing".format(id),'Business Error', FNummer), HTTPStatus.NOT_FOUND

        db.session.delete(partyIndiv)
        db.session.commit()
        logger.info("Party with ID {} deleted".format(id))
        return {}, HTTPStatus.NO_CONTENT

    @swag_from('TMF632PartyIndiv_V1.yaml', endpoint='/individual/{id}', methods=['GET'])
    def get(self, id):

        partyIndiv = Individual.get_by_id(indiv_id=id)

        if partyIndiv is None:
            logger.warning(errorFormaterMarshmallow(400,'On get EP', None, "Party ID {} not exsiting".format(id)))
            return errorFormaterMarshmallow(400,'On get EP', None, "Party ID {} not exsiting".format(id)), HTTPStatus.NOT_FOUND

        return IndivTMF632_Schema.dump(partyIndiv), HTTPStatus.OK

    @swag_from('TMF632PartyIndiv_V1.yaml', endpoint='/individual/{id}', methods=['PATCH'])
    @isValidJSON
    def patch(self, id):
        partyIndiv = Individual.get_by_id(indiv_id=id)
        if partyIndiv is None:
            FNummer = FBNRPREFIX + '00000009'
            logger.warning(errorFormaterMarshmallow(400, 'On patch EP', None, "Party ID {} not exsiting".format(id)),
                           extra={'fehlerbildnummer': FNummer, 'incomming_message': id,
                                  'communication_pattern': 'req-reply', 'service_domain': 'party',
                                  'service_call': request.url})
            return errorFormaterMarshmallow(400, 'On patch EP', None, "Party ID {} not existing".format(id),
                                            'Business Error', FNummer), HTTPStatus.NOT_FOUND

        json_data = request.get_json()
        # pick up all different root Elements from requested Json
        indivJson= catch_Json(json_data, 'root')
        mediumJson = catch_Json(json_data, 'medium')
        CharJson = catch_Json(json_data, 'character')
        relPartyJson = catch_Json(json_data, 'relparty')

        if indivJson:
            try:
                ## to use Indiv Schema validation we must guarant that familyName and givenName are part of JSON.
                ## Consumer of that API EP must not deliver both Value for patch. Therfore we add these Fields to indivJson
                ## with original Value in case of not delivered.
                fam = indivJson.setdefault('familyName', "")
                if fam =="":
                    indivJson['familyName']= partyIndiv.familyName
                givN = indivJson.setdefault('givenName', "")
                if givN =="":
                    indivJson['givenName'] = partyIndiv.givenName

                data = Individual_Schema.load(data=indivJson)
            except ValidationError as errors:
                FNummer = FBNRPREFIX + '00000004'
                logger.error(errorFormaterMarshmallow(400, 'Validation errors', errors),
                             extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                    'communication_pattern': 'req-reply', 'service_domain': 'party',
                                    'service_call': request.url})
                return errorFormaterMarshmallow(400, 'Validation errors', errors,
                                                'mandatory Values for Individual Json not delivered', 'Business Error',
                                                FNummer), HTTPStatus.BAD_REQUEST
            ## setting now update Fields
            for key, value in indivJson.items():
                if value is None:
                    setattr(partyIndiv, key, None)
                else:
                    setattr(partyIndiv, key, value)
            # start set ORM Session Object
            db.session.add(partyIndiv)
        if CharJson:
            if checkUniqueBusinessID(CharJson, 'partyCharacteristic',method="patch") is True:
                FNummer = FBNRPREFIX + '00000003'
                logger.error("http code 400, Business Key violation at partyCharResacteristic",
                             extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                    'communication_pattern': 'req-reply', 'service_domain': 'party',
                                    'service_call': request.url})
                return errorFormaterMarshmallow(400, 'Business Key violation at partyCharResacteristic', None,
                                                'name for partyCharResacteristic can only exist once per each party',
                                                'Business Error', FNummer), HTTPStatus.BAD_REQUEST

            #patch request delivered related Party Data. RFC7386 defined that target request overwrites all
            for i in range(0,len(partyIndiv.characteristic)):
                partyCharRes= Characterstic.get_by_id(partyIndiv.characteristic[i].id)
                db.session.delete(partyCharRes)

            for char in CharJson:
                char = load_json(char)
                #with that we follow rfc7386 approach
                if char['name'] is None:
                    continue
                try:
                    dataM = Characteristic_Schema.load(data=char)
                except ValidationError as errors:
                    FNummer = FBNRPREFIX + '00000007'
                    logger.info(errorFormaterMarshmallow(400, 'Validation errors', errors),
                                extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                       'communication_pattern': 'req-reply', 'service_domain': 'party',
                                       'service_call': request.url})
                    return errorFormaterMarshmallow(400, 'Validation errors', errors,
                                                    'validation for party Character with error', 'Business Error',
                                                    FNummer), HTTPStatus.BAD_REQUEST

                partyCharRes = Characterstic(dataM, partyIndiv)
                db.session.add(partyCharRes)
        if relPartyJson:
            if mediumJson and checkUniqueBusinessID(mediumJson, 'relatedParty',method="patch") is True:
                    FNummer = FBNRPREFIX + '00000002'
                    logger.error("http code 400, Business Key violation at relatedParty",
                                 extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                        'communication_pattern': 'req-reply', 'service_domain': 'party',
                                        'service_call': request.url})
                    return errorFormaterMarshmallow(400, 'Business Key violation at relatedParty', None,
                                                    'id for Related Party can only exist once per each party and must have valid Value',
                                                    'Business Error', FNummer), HTTPStatus.BAD_REQUEST

            #patch request delivered related Party Data. RFC7386 defined taht
            for i in range(0,len(partyIndiv.relatedparty)):
                relPartyRes= RelatedParty.get_by_id(partyIndiv.relatedparty[i].id_tech)
                db.session.delete(relPartyRes)

            for rel in relPartyJson:
                rel = load_json(rel)
                #with that we follow rfc7386 approach
                if rel['id'] is None:
                    continue
                try:
                    dataM = RelatedParty_Schema.load(data=rel)
                except ValidationError as errors:
                    print ("Exeption on RelParty Schema")
                    FNummer = FBNRPREFIX + '00000008'
                    logger.info(errorFormaterMarshmallow(400, 'Validation errors',errors),
                                extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                       'communication_pattern': 'req-reply', 'service_domain': 'party',
                                       'service_call': request.url})
                    return errorFormaterMarshmallow(400, 'Validation errors',errors,
                                                    'validation for related party Character with error',
                                                    'Business Error',
                                                    FNummer), HTTPStatus.BAD_REQUEST

                relPartyRes = RelatedParty(dataM, partyIndiv)
                db.session.add(relPartyRes)

        if mediumJson:
            # now check if Business Key for medium, relatedParty and Character are unique
            if mediumJson and checkUniqueBusinessID(mediumJson, 'medium', method="patch") is True:
                FNummer = FBNRPREFIX + '00000001'
                logger.error("http code 400, Business Key violation at contactMedium",
                             extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                    'communication_pattern': 'req-reply', 'service_domain': 'party',
                                    'service_call': request.url})
                return errorFormaterMarshmallow(400, 'Business Key violation at contactMedium', None,
                                                'mediumType for contactMedium can only exist once per each party',
                                                'Business Error', FNummer), HTTPStatus.BAD_REQUEST

            for i in range(0,len(partyIndiv.contactmedium)):
                contactMediumRes = ContactMedium.get_by_id(partyIndiv.contactmedium[i].id)
                db.session.delete(contactMediumRes)

            for med in mediumJson:
                med= load_json(med)
                #with that we follow rfc7386 approach
                if med['mediumType'] is None:
                    continue
                try:
                    dataM= Medium_Schema.load(data=med)
                except ValidationError as errors:
                    FNummer = FBNRPREFIX + '00000006'
                    logger.error(errorFormaterMarshmallow(400, 'Validation errors', errors),
                                 extra={'fehlerbildnummer': FNummer, 'incomming_message': json_data,
                                        'communication_pattern': 'req-reply', 'service_domain': 'party',
                                        'service_call': request.url})
                    return errorFormaterMarshmallow(400, 'Validation errors', errors,
                                                    'validation for medium with error', 'Business Error',
                                                    FNummer), HTTPStatus.BAD_REQUEST

                contactMediumRes = ContactMedium(dataM,partyIndiv)
                db.session.add(contactMediumRes)
        #### ORM Session Context finished
        db.session.commit()
        logger.info("Party with ID {} patched".format(id))
        partyIndiv = Individual.get_by_id(partyIndiv.id)
        return IndivTMF632_Schema.dump(partyIndiv), HTTPStatus.OK

def catch_Json(json_data, part):

    if part == "root":
        # Take root Values for class Individual from requested Json
        indivJson = load_json(json_data)
        return  indivJson
    # Ckeck if there is ContactMedium
    elif part == "medium":
        try:
            mediumJson = json_data['contactMedium']
            return mediumJson
        except:
            return {}
    # Ckeck if there is Characteristic
    elif part == "character":
        try:
            CharJson = json_data['partyCharacteristic']
            return CharJson
        except:
            return {}
    # Ckeck if there is relatedParty
    elif part == "relparty":
        try:
            relPartyJson = json_data['relatedParty']
            return relPartyJson
        except:
            return {}

def checkUniqueBusinessID(liste,type,method):
    checkList=[]
    if type =='relatedParty':
        BusinessID= 'id'
    elif type =='medium':
        BusinessID = 'mediumType'
    elif type =='partyCharacteristic':
        BusinessID = 'name'

    for i in range(0, len(liste)):
        #Business Key must have Value != None
        if liste[i][BusinessID] is not None and liste[i][BusinessID] !="":
            checkList.append(liste[i][BusinessID])
        else:
            if method != 'patch': #in case of patch we can delete Object with delivering none
                return True #true means Business ID violation
    twice=listDupsUnique(checkList)
    if twice:
        return True
    else:
        return False # no Business ID violation

def listDupsUnique(listNums):
    return list(unique_everseen(duplicates(listNums)))#deletes duplicate Values
