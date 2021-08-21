from marshmallow import Schema, fields, validate, validates, ValidationError
import re
#from schemas.comCharracteristic import ComChar_Schema

class MediumSchema(Schema):
    class Meta:
        ordered = True

    mediumType = fields.String()
    preferred = fields.Boolean(required=False)
    mediumVerified= fields.Boolean(required=False)
    city = fields.String(required=False)
    contactType = fields.String(required=False)
    country = fields.String(required=False)
    emailAddress = fields.String(required=False)
    faxNumber = fields.String(required=False)
    phoneNumber = fields.String(required=False)
    postCode = fields.String(required=False)
    socialNetworkId = fields.String(required=False)
    stateOrProvince = fields.String(required=False)
    street1 = fields.String(required=False)
    houseNumber=fields.String(required=False)
    houseNumberAppendix=fields.String(required=False)
    street2 = fields.String(required=False)
    #baseType = fields.String(required=False)
    #schemaLocation = fields.String(required=False)
    #type = fields.String(required=False)
    endDateTime = fields.String(required=False)
    startDateTime = fields.String(required=False)

    @validates('mediumType')
    def validate_mediumType(self, value):
        if value not in ['EMAIL', 'FIXED_LINE', 'MOBILE', 'ADDRESS', 'SOCIAL', 'FAX']:
            raise ValidationError('Invalid Medium Type delivered')
    @validates('emailAddress')
    def check(self, value):
        if value!='':
            regex = '^[A-Za-z0-9]+[\._-]?[A-Za-z0-9]+[@]\w+[.]\w{2,3}$'
            if (re.search(regex, value)):
                print("Valid Email")
            else:
                raise ValidationError('Invalid EMail Address')
class contMedtoTMF_Schema(Schema):
    class Meta:
        ordered = True

    mediumType = fields.String(dump_only=True)
    preferred = fields.Boolean(dump_only=True)
    #baseType = fields.String(dump_only=True)
    #schemaLocation = fields.String(dump_only=True)
    #type = fields.String(dump_only=True)
    #this doesn't work
    #characteristic = fields.Nested(ComChar_Schema, attribute='contactmedium', dump_only=True)
    #choose that solution
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

