from marshmallow import Schema, fields, validates, ValidationError

class CharacteristicSchema(Schema):
    class Meta:
        ordered = True

    name = fields.String()
    valueType = fields.String(required=False)
    value = fields.String()

    #baseType = fields.String(required=False, missing='PartyChar')
    #schemaLocation = fields.String(required=False)
    #type = fields.String(required=False, missing='Character')

    @validates('name')
    def validate_Name(self, value):
        if value =='':
            raise ValidationError("Party Character missing: Name")
    @validates('value')
    def validate_value(self, value):
        if value =='':
            raise ValidationError("Party Character missing: Value")