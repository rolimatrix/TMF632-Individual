# coding=utf-8
from marshmallow import Schema, fields, validates, ValidationError

class RelatedPartySchema(Schema):
    class Meta:
        ordered = True
    id = fields.String(required=True)
    href = fields.String(required=False,allow_none=True)
    name = fields.String(required=False,allow_none=True)
    role = fields.String(required=False,allow_none=True)

    @validates('id')
    def validate_id(self, value):
       if value == '':
          raise ValidationError("Related Party missing: id")

class manyRelatedPatySchema(Schema):
    data= fields.Nested(RelatedPartySchema, attribute='items',many=True)