# coding=utf-8
from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class MediumSchema(Schema):
    class Meta:
        ordered = True
    mediumType = fields.String(required=True)
    preferred = fields.Boolean(required=False)
    mediumVerified= fields.Boolean(required=False,allow_none=True)
    city = fields.String(required=False,allow_none=True)
    contactType = fields.String(required=False,allow_none=True)
    country = fields.String(required=False,allow_none=True)
    emailAddress = fields.String(required=False,allow_none=True)
    faxNumber = fields.String(required=False,allow_none=True)
    phoneNumber = fields.String(required=False,allow_none=True)
    postCode = fields.String(required=False,allow_none=True)
    socialNetworkId = fields.String(required=False,allow_none=True)
    stateOrProvince = fields.String(required=False,allow_none=True)
    street1 = fields.String(required=False,allow_none=True)
    houseNumber=fields.String(required=False,allow_none=True)
    houseNumberAppendix=fields.String(required=False,allow_none=True)
    street2 = fields.String(required=False,allow_none=True)
    endDateTime = fields.String(required=False,allow_none=True)
    startDateTime = fields.String(required=False,allow_none=True)

    @validates('mediumType')
    def validate_mediumType(self, value):
        if value not in ['EMAIL', 'FIXED_LINE', 'MOBILE', 'ADDRESS', 'SOCIAL', 'FAX']:
            raise ValidationError('Invalid Medium Type delivered')

    @validates('emailAddress')
    def check(self, value):
        if value!='':
            regex = '^[A-Za-z0-9]+[\._-]?[A-Za-z0-9.-]+[@]\w+[.]\w{2,3}$'
            if not (re.search(regex, value)):
                raise ValidationError('Invalid EMail Address')

class contMedtoTMF_Schema(Schema):
    class Meta:
        ordered = True

    mediumType = fields.String(dump_only=True)
    preferred = fields.Boolean(dump_only=True)
    characteristic = fields.Method(serialize='JsonCharFields')
    validFor = fields.Method(serialize='JsonValidField')


    def JsonCharFields(self, partyIndiv):
        characters = {
                'contactType': partyIndiv.contactType,
                'emailAddress': partyIndiv.emailAddress,
                'city': partyIndiv.city,
                'street1': partyIndiv.street1,
                'houseNumber': partyIndiv.houseNumber,
                'houseNumberAppendix': partyIndiv.houseNumberAppendix,
                'street2': partyIndiv.street2,
                'country': partyIndiv.country,
                'phoneNumber':partyIndiv.phoneNumber,
                'faxNumber': partyIndiv.faxNumber,
                'postCode': partyIndiv.postCode,
                'stateOrProvince':partyIndiv.stateOrProvince,
                'socialNetworkId':partyIndiv.socialNetworkId,
                'stateOrProvince': partyIndiv.stateOrProvince
        }

        return characters

    def JsonValidField(self, partyIndiv):
        characters = {
                'startDateTime': partyIndiv.startDateTime,
                'endDateTime': partyIndiv.endDateTime,
        }
        return characters

