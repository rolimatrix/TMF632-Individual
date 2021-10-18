from marshmallow import Schema, fields, validate, validates, ValidationError
from schemas.medium import contMedtoTMF_Schema
from schemas.characteristic import CharacteristicSchema
from schemas.relatedParty import RelatedPartySchema
from flask import request

class IndividualSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    status = fields.String(required=False)
    aristocraticTitle = fields.String(required=False)
    birthDate = fields.String(required=False)
    countryOfBirth= fields.String(required=False)
    deathDate = fields.String(required=False)
    familyName = fields.String()
    givenName = fields.String()
    familyNamePrefix = fields.String(required=False)
    formattedName = fields.String(required=False)
    fullName=fields.String(required=False)
    gender=fields.String(required=False)
    generation=fields.String(required=False)
    legalName=fields.String(required=False)
    location=fields.String(required=False)
    maritalStatus=fields.String(required=False)
    middleName=fields.String(required=False)
    nationality=fields.String(required=False)
    placeOfBirth=fields.String(required=False)
    preferredGivenName=fields.String(required=False)
    title=fields.String(required=False)

    @validates('status')
    def validate_status(self, value):
        if value not in ['initialized', 'validated', 'deceased']:
            raise ValidationError('Invalid Status of PartyIndividual')

    @validates('familyName')
    def validate_familyName(self, value):
        if value =='':
            raise ValidationError('Family Name requires Value != empty')
    @validates('givenName')
    def validate_givenName(self, value):
        if value =='':
            raise ValidationError('given Name requires Value != empty')

#for deserializing
class IndivtoTMF(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    href= fields.Method(serialize='buildHref')

    status = fields.Str()
    aristocraticTitle = fields.String(dump_only=True)
    birthDate = fields.String(dump_only=True)
    countryOfBirth = fields.String(dump_only=True)
    deathDate = fields.String(dump_only=True)
    familyName = fields.String(dump_only=True)
    givenName = fields.String(dump_only=True)
    familyNamePrefix = fields.String(dump_only=True)
    formattedName = fields.String(dump_only=True)
    fullName = fields.String(dump_only=True)
    gender = fields.String(dump_only=True)
    generation = fields.String(dump_only=True)
    legalName = fields.String(dump_only=True)
    location = fields.String(dump_only=True)
    maritalStatus = fields.String(dump_only=True)
    middleName = fields.String(dump_only=True)
    nationality = fields.String(dump_only=True)
    placeOfBirth = fields.String(dump_only=True)
    preferredGivenName = fields.String(dump_only=True)
    title = fields.String(dump_only=True)
    contactMedium = fields.Nested(contMedtoTMF_Schema, attribute='contactmedium',dump_only=True,many=True)
    partyCharacteristic= fields.Nested(CharacteristicSchema, attribute='characteristic',dump_only=True,many=True)
    relatedParty = fields.Nested(RelatedPartySchema, attribute='relatedparty', dump_only=True, many=True)

    def buildHref(self,partyIndiv):
        url = request.url
        if str(partyIndiv.id) not in url:
            url = "{}/{}".format(url, partyIndiv.id)

        return url