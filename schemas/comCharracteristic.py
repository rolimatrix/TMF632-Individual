from marshmallow import Schema, fields


class ComChar_Schema(Schema):
    class Meta:
        ordered = True

    city = fields.String(dump_only=True)
    contactType = fields.String(dump_only=True)
    country = fields.String(dump_only=True)
    emailAddress = fields.String(dump_only=True)
    faxNumber = fields.String(dump_only=True)
    phoneNumber = fields.String(dump_only=True)
    postCode = fields.String(dump_only=True)
    socialNetworkId = fields.String(dump_only=True)
    stateOrProvince = fields.String(dump_only=True)
    street1 = fields.String(dump_only=True)
    houseNumber=fields.String(dump_only=True)
    houseNumberAppendix=fields.String(dump_only=True)
    street2 = fields.String(dump_only=True)