from marshmallow import Schema, fields, validates, ValidationError

class CharacteristicSchema(Schema):
    class Meta:
        ordered = True

    name = fields.String()
    valueType = fields.String(required=False)
    value = fields.String()

    @validates('name')
    def validate_Name(self, value):
        if value =='':
            raise ValidationError("Party Character missing: Name")
    @validates('value')
    def validate_value(self, value):
        if value =='':
            raise ValidationError("Party Character missing: Value")