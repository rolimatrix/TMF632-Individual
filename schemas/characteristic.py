# coding=utf-8
from marshmallow import Schema, fields, validates, ValidationError

class CharacteristicSchema(Schema):
    class Meta:
        ordered = True

    name = fields.String(required=True)
    valueType = fields.String(required=False,allow_none=True)
    value = fields.String(required=True)

    @validates('name')
    def validate_Name(self, value):
        if value =='':
            raise ValidationError("Party Character missing: Name")
    @validates('value')
    def validate_value(self, value):
        if value =='':
            raise ValidationError("Party Character missing: Value")