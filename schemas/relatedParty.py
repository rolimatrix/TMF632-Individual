from marshmallow import Schema, fields, validates, ValidationError
from flask import request

class RelatedPartySchema(Schema):
    class Meta:
        ordered = True
    id = fields.String()
    href = fields.String(required=False)
    name = fields.String(required=False)
    role = fields.String(required=False)

    @validates('id')
    def validate_id(self, value):
       if value == '':
          raise ValidationError("Related Party missing: Id")