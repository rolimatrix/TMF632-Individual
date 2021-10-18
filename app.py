import os
from flask import Flask
from flask_restful import Api, Resource
from flask_script import Manager
#from flask_script._compat import text_type

from flask_migrate import Migrate, MigrateCommand

from flask_cors import CORS

from flasgger import Swagger

from ressource.party import Party, PartyId
from ressource.health import Health
from extensions import db


def create_app():
    app = Flask(__name__)

    env = os.environ.get('ENV', 'Development')
    if env == "Production":
        config_str = 'config.ProductionConfig'
    elif env == "Staging":
        config_str = 'config.StagingConfig'
    elif env == "Development":
        config_str = 'config.DevelopmentConfig'
   
    app = Flask(__name__)
    app.config.from_object(config_str)
    #app.config.from_pyfile('config.py')

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    manager= Manager(app)
    db.create_all(app=app)
    manager.add_command('db', MigrateCommand)
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



if __name__ == "__main__":
    app = create_app()
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0')
