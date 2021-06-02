from flask import Flask
from flask_restful import Api, Resource
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flask_cors import CORS

from flasgger import Swagger

from ressource.party import Party, PartyId
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    manager= Manager(app)
    manager.add_command('db', MigrateCommand)
    app.config['SWAGGER'] = {
        'title': 'Giga Party Individual',
        'uiversion': 2
        }
    swag = Swagger(app, template_file='./conf/swagger/TMF632PartyIndiv_V1.yaml')

    CORS(app)



def register_resources(app):
    api = Api(app)
    api.add_resource(Party, '/party-management-individual/individual')
    api.add_resource(PartyId, '/party-management-individual/individual/<int:id>')


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
