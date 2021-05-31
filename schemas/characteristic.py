from marshmallow import Schema, fields, ValidationError, validate,missing


class CharacteristicSchema(Schema):
    class Meta:
        ordered = True

    name = fields.String(required=True, error_messages={"required": "Party Character missing: Name"})
    name = fields.String(required=True, validate=validate.Length(min=1), error_messages={"required": "Party Character Name without content"})

    valueType = fields.String(required=False)
    value = fields.String(required=True, validate=validate.Length(min=1),error_messages={"required": "Party Character missing: Value"})

    baseType = fields.String(required=False, missing='PartyChar')
    schemaLocation = fields.String(required=False)
    type = fields.String(required=False, missing='Character')