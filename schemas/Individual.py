from marshmallow import Schema, fields, validate
from schemas.medium import contMedtoTMF_Schema
from flask import request

class IndividualSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    status = fields.String(required=True)
    aristocraticTitle = fields.String(required=True)
    birthDate = fields.String(required=False)
    countryOfBirth= fields.String(required=False)
    deathDate = fields.String(required=False)
    familyName = fields.String(required=True)
    givenName = fields.String(required=True)
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




class IndivtoTMF(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    href= fields.Method(serialize='buildHref')

    status = fields.Str(validate=validate.OneOf(["initialized","validated","deceaded "]))
    aristocraticTitle = fields.String(required=True)
    birthDate = fields.String(required=False)
    countryOfBirth = fields.String(required=False)
    deathDate = fields.String(required=False)
    familyName = fields.String(required=True)
    givenName = fields.String(required=True)
    familyNamePrefix = fields.String(required=False)
    formattedName = fields.String(required=False)
    fullName = fields.String(required=False)
    gender = fields.String(required=False)
    generation = fields.String(required=False)
    legalName = fields.String(required=False)
    location = fields.String(required=False)
    maritalStatus = fields.String(required=False)
    middleName = fields.String(required=False)
    nationality = fields.String(required=False)
    placeOfBirth = fields.String(required=False)
    preferredGivenName = fields.String(required=False)
    title = fields.String(required=False)
    contactMedium = fields.Nested(contMedtoTMF_Schema, attribute='contactmedium',dump_only=True,many=True)

    def buildHref(self,partyIndiv):
        url = request.url
        characters = "{}/{}".format(url, partyIndiv.id)
        return characters