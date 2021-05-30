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
from model.othername import OtherName
from model.skill import Skill
from model.externalreference import ExternalReference

from schemas.Individual import IndividualSchema, IndivtoTMF
from schemas.medium import MediumSchema

Individual_Schema = IndividualSchema()
IndivTMF632_Schema= IndivtoTMF()

Medium_Schema = MediumSchema()

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

        json_data = request.get_json()

        #Take root Values for class Individual from requested Json
        indivJson=load_json(json_data)

        #Ckeck if thers is ContactMedium
        try:
            medium = json_data['contactMedium']
            contact_exist= True
        except:
            contact_exist= False

        #check Json for Individual
        try:
            data = Individual_Schema.load(data=indivJson)
            partyIndiv = Individual(**data)
            partyIndiv.save()

        except ValidationError as errors:
            return {'message': 'Validation errors', 'errors': errors.messages}, HTTPStatus.BAD_REQUEST

        if contact_exist:
            #it could be that we have more then one Contact
            for m in medium:
                # Make Contact Medium flat (without dictionary Characterstic and valid)
                medium= load_json(m)
                try:
                    dataM = Medium_Schema.load(data=medium)
                    partyContact = ContactMedium(**dataM)
                    partyContact.fk_idIndiv = partyIndiv.id
                    partyContact.save()
                except ValidationError as errors:
                    return {'message': 'Validation errors', 'errors': errors.messages}, HTTPStatus.BAD_REQUE

        partyIndiv = Individual.get_by_id(partyIndiv.id)

        return IndivTMF632_Schema.dump(partyIndiv), HTTPStatus.OK


class PartyId(Resource):
    @swag_from('TMF632PartyIndiv_V1.yml', endpoint='/individual/{id}', methods=['DELETE'])
    def delete(self, id):
        partyIndiv = Individual.get_by_id(indiv_id=id)

        if partyIndiv is None:
            return {'message': 'Party not found'}, HTTPStatus.NOT_FOUND

        partyIndiv.delete()
        return {}, HTTPStatus.NO_CONTENT

    @swag_from('TMF632PartyIndiv_V1.yml', endpoint='/individual/{id}', methods=['GET'])
    def get(self, id):
        partyIndiv = Individual.get_by_id(indiv_id=id)

        if partyIndiv is None:
            return {'message': 'Party not found'}, HTTPStatus.NOT_FOUND

        return IndivTMF632_Schema.dump(partyIndiv), HTTPStatus.OK