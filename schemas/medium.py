from marshmallow import Schema, fields
#from schemas.comCharracteristic import ComChar_Schema

class MediumSchema(Schema):
    class Meta:
        ordered = True

    mediumType = fields.String(required=False)
    preferred = fields.Boolean(required=False)
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
    street2 = fields.String(required=False)
    baseType = fields.String(required=True)
    schemaLocation = fields.String(required=False)
    type = fields.String(required=True)
    endDateTime = fields.String(required=False)
    startDateTime = fields.String(required=False)

class contMedtoTMF_Schema(Schema):
    class Meta:
        ordered = True

    mediumType = fields.String(dump_only=True)
    preferred = fields.Boolean(dump_only=True)
    baseType = fields.String(dump_only=True)
    schemaLocation = fields.String(dump_only=True)
    type = fields.String(dump_only=True)
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

