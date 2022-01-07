# coding=utf-8
import os
from marshmallow import Schema, fields, validate, validates, ValidationError
from schemas.medium import contMedtoTMF_Schema
from schemas.characteristic import CharacteristicSchema
from schemas.relatedParty import RelatedPartySchema
from flask import request
dbUSER=os.environ.get('SPRING_DATASOURCE_USERNAME')

class IndividualSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    status = fields.String(required=False)
    aristocraticTitle = fields.String(required=False,allow_none=True)
    birthDate = fields.String(required=False,allow_none=True)
    countryOfBirth= fields.String(required=False,allow_none=True)
    deathDate = fields.String(required=False,allow_none=True)
    familyName = fields.String(required=True)
    givenName = fields.String(required=True)
    familyNamePrefix = fields.String(required=False,allow_none=True)
    formattedName = fields.String(required=False,allow_none=True)
    fullName=fields.String(required=False,allow_none=True)
    gender=fields.String(required=False,allow_none=True)
    generation=fields.String(required=False,allow_none=True)
    legalName=fields.String(required=False,allow_none=True)
    location=fields.String(required=False,allow_none=True)
    maritalStatus=fields.String(required=False,allow_none=True)
    middleName=fields.String(required=False,allow_none=True)
    nationality=fields.String(required=False,allow_none=True)
    placeOfBirth=fields.String(required=False,allow_none=True)
    preferredGivenName=fields.String(required=False,allow_none=True)
    title=fields.String(required=False,allow_none=True)

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
    contactMedium = fields.Nested(contMedtoTMF_Schema, attribute="contactmedium",dump_only=True,many=True)
    partyCharacteristic= fields.Nested(CharacteristicSchema, attribute="characteristic",dump_only=True,many=True)
    relatedParty = fields.Nested(RelatedPartySchema, attribute="relatedparty", dump_only=True, many=True)

    def buildHref(self,partyIndiv):
        url = request.url
        if str(partyIndiv.id) not in url:
            url = "{}/{}".format(url, partyIndiv.id)

        return url