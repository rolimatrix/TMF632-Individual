from flask import request, current_app
from flask_restful import Resource
import time

#@app.route('/party-management-individual/healthz')
class Healthz(Resource):
    def get (self):
        return "OK"


#@app.route('/party-management-individual/healthx')
class Healthx(Resource):
    def get (self):
        time.sleep(1);
        return "OK"