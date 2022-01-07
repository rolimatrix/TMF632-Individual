# coding=utf-8
from flask_restful import Resource

class Health(Resource):
    def get (self):
        return "OK"