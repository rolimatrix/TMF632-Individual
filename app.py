# coding=utf-8
import os
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flasgger import Swagger
from ressource.party import Party, PartyId
from ressource.health import Health
from extensions import db
import traceback
from sqlalchemy import create_engine


from conf import _init_logging

# get global Fehlerbildnummer Prefix as ENV Variable
FBNRPREFIX = os.environ.get('FBNRPREFIX', '99999999')

def create_app():

    env = os.environ.get('ENV', 'Staging')

    if env == "Production":
        config_str = 'config.ProductionConfig'
    elif env == "Staging":
        config_str = 'config.StagingConfig'
    elif env == "Development":
        config_str = 'config.DevelopmentConfig'

    logger.info("Running on Environment {}".format(env))
    app = Flask(__name__)
    app.config.from_object(config_str)
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    try:
        db.init_app(app)
        migrate = Migrate(app, db)
    except:
        FBNRPREFIX= FBNRPREFIX + '00000010'
        logger.error('DB Init Error:' + traceback.print_exc(), extra={'fehlerbildnummer': FNummer, 'incomming_message': "",
                              'communication_pattern': '', 'service_domain': 'party',
                              'service_call': ""})

    try:
        dbUSER = os.environ.get('SPRING_DATASOURCE_USERNAME')
        # Create schema
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        if not engine.dialect.has_schema(engine, dbUSER):
            engine.execute('CREATE SCHEMA IF NOT EXISTS %s' % dbUSER)

        db.create_all(app=app)


    except:
        FBNRPREFIX = FBNRPREFIX + '00000011'
        logger.error('DB Create Error:' + traceback.print_exc(),
                     extra={'fehlerbildnummer': FNummer, 'incomming_message': "",
                            'communication_pattern': '', 'service_domain': 'party',
                            'service_call': ""})

    app.config['SWAGGER'] = {
        'title': 'Giga Party Individual',
        'uiversion': 2
        }
    swag = Swagger(app, template_file='./conf/swagger/TMF632PartyIndiv_V1.yaml')

    CORS(app)

def register_resources(app):
    api = Api(app)
    api.add_resource(Party, '/party/v1/individual')
    api.add_resource(Health, '/actuator/health')
    api.add_resource(PartyId, '/party/v1/individual/<int:id>')
    @app.route("/")
    def hello():
        return "Hello here is Python based R.Schier Party-Individual  APP"

if __name__ == "__main__":

    # init logging
    logger = _init_logging('main.app')

    app = create_app()
    env = os.environ.get('ENV', 'Staging')

    if env == 'Staging':
        print ("I am in Staging Mode")

    app.run(debug=True, host='0.0.0.0', port=8080)
