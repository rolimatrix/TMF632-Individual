from flask import request, current_app
from flask_restful import Resource

class Health(Resource):
    def get (self):
        return "OK"