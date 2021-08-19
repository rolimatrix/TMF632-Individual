import os

DEBUG = False

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://py_rschier:FCBayern00@localhost:5432/partyindiv'

SECRET_KEY= '311d4b5499e945398f6edf147a34666f'