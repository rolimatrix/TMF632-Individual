import jsons

from flask import request, current_app
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

Individual_Schema = IndividualSchema()
IndivTMF632_Schema= IndivtoTMF()
Medium_Schema = MediumSchema()
Characteristic_Schema = CharacteristicSchema()
RelatedParty_Schema = RelatedPartySchema()

def load_json(json_data):
    output_dict = {}
    for key, value in json_data.items():
        if not type(value) == list:
            if type(value) == dict:
                for keyD, valueD in value.items():
                    if type(valueD)== str:
                        k=keyD.replace("@", "")
                        output_dict[k] = valueD
            elif type(value)== str or type(value)== bool:
                k=key.replace("@", "")
                output_dict[k] = value
    return output_dict

class Party(Resource):

    @swag_from('TMF632PartyIndiv_V1.yml',endpoint='individual', methods=['POST'])

    def post(self):
        # check if request is well formed Json
        try:
            json_data = request.get_json()
        except:
            return errorFormaterMarshmallow(400, 'Validation errors'), HTTPStatus.BAD_REQUEST

        indivJson= catch_Json(json_data, 'root')
        # check Json for Individual
        try:
            data = Individual_Schema.load(data=indivJson)
            partyIndiv = Individual(**data)
            partyIndiv.save()
        except ValidationError as errors:
            return errorFormaterMarshmallow(400,'Validation errors',errors), HTTPStatus.BAD_REQUEST

        mediumJson = catch_Json(json_data, 'medium')
        if mediumJson:
            #it could be that we have more then one Contact
            for m in mediumJson:
                # Make Contact Medium flat (without dictionary Characterstic and valid)
                medium= load_json(m)
                try:
                    dataM = Medium_Schema.load(data=medium)
                    partyContact = ContactMedium(**dataM)
                    partyContact.fk_idIndiv = partyIndiv.id
                    partyContact.save()
                except ValidationError as errors:
                    partyIndiv.delete()
                    return errorFormaterMarshmallow(400,'Validation errors',errors), HTTPStatus.BAD_REQUEST

        CharJson = catch_Json(json_data, 'character')
        if CharJson:
            # it could be that we have more then one characteristic
            for ch in CharJson:
                character = load_json(ch)
                try:
                    dataM = Characteristic_Schema.load(data=character)
                    partyChar = Characterstic(**dataM)
                    partyChar.fk_idIndiv = partyIndiv.id
                    partyChar.save()
                except ValidationError as errors:
                    partyIndiv.delete()
                    return errorFormaterMarshmallow(400,'Validation errors',errors), HTTPStatus.BAD_REQUEST

        relPartyJson = catch_Json(json_data, 'relparty')
        if relPartyJson:
            # it could be that there are more then one relParty existent
            for rel in relPartyJson:
                rel= load_json(rel)
                try:
                    dataM = RelatedParty_Schema.load(data=rel)
                    relParty= RelatedParty(**dataM)
                    relParty.fk_idIndiv = partyIndiv.id
                    relParty.save()
                except ValidationError as errors:
                    partyIndiv.delete()
                    return errorFormaterMarshmallow(400,'Validation errors',errors), HTTPStatus.BAD_REQUEST

        partyIndiv = Individual.get_by_id(partyIndiv.id)

        return IndivTMF632_Schema.dump(partyIndiv), HTTPStatus.OK


class PartyId(Resource):
    @swag_from('TMF632PartyIndiv_V1.yml', endpoint='/individual/{id}', methods=['DELETE'])
    def delete(self, id):
        partyIndiv = Individual.get_by_id(indiv_id=id)

        if partyIndiv is None:
            return errorFormaterMarshmallow(400, 'Party not found'), HTTPStatus.NOT_FOUND

        partyIndiv.delete()
        return {}, HTTPStatus.NO_CONTENT

    @swag_from('TMF632PartyIndiv_V1.yml', endpoint='/individual/{id}', methods=['GET'])
    def get(self, id):
        partyIndiv = Individual.get_by_id(indiv_id=id)

        if partyIndiv is None:
            return errorFormaterMarshmallow(400, 'Party not found'), HTTPStatus.NOT_FOUND

        return IndivTMF632_Schema.dump(partyIndiv), HTTPStatus.OK

    @swag_from('TMF632PartyIndiv_V1.yml', endpoint='/individual/{id}', methods=['PATCH'])
    def patch(self, id):
        partyIndiv = Individual.get_by_id(indiv_id=id)
        if partyIndiv is None:
            return errorFormaterMarshmallow(400, 'Party not found'), HTTPStatus.NOT_FOUND

        # check if request is well formed Json
        try:
            json_data = request.get_json()
        except:
            return errorFormaterMarshmallow(400, 'Validation errors'), HTTPStatus.BAD_REQUEST

        indivJson = catch_Json(json_data, 'root')
        # check Json for Individual
        try:
            data = Individual_Schema.load(data=indivJson)
            partyIndiv = Individual(**data)
            partyIndiv.save()
            return IndivTMF632_Schema.dump(partyIndiv), HTTPStatus.OK
        except ValidationError as errors:
            return errorFormaterMarshmallow(400, 'Validation errors', errors), HTTPStatus.BAD_REQUEST

'''        
        
        for key, value in json_data.items():
            if not type(value) == list and not type(value) == dict:
                if value is None:
                    partyIndiv.key = ""
                else:
                    #print (type(partyIndiv))
                    partyIndiv.key = value
                    print (partyIndiv.key)

        #partyIndiv.aristocraticTitle =json_data.get('aristocraticTitle') or partyIndiv.aristocraticTitle
        #partyIndiv.familyName = json_data.get('familyName') or partyIndiv.familyName
        #partyIndiv.givenName = json_data.get('givenName') or partyIndiv.givenName

        partyIndiv.save()
        return IndivTMF632_Schema.dump(partyIndiv), HTTPStatus.OK
'''
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