# coding=utf-8
import os

class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
   
class DevelopmentConfig(Config):
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')
    #SQLALCHEMY_DATABASE_URI='postgresql://py_rschier:FCBayern00@localhost:5432/partyindiv'
    dbPWD = os.environ.get('SPRING_DATASOURCE_PASSWORD')
    dbUSER = os.environ.get('SPRING_DATASOURCE_USERNAME')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@localhost:5432/partyindiv'.format(dbUSER,dbPWD)

class StagingConfig(Config):
    SECRET_KEY = os.urandom(24)
    dbPWD= os.environ.get('SPRING_DATASOURCE_PASSWORD')
    dbUSER=os.environ.get('SPRING_DATASOURCE_USERNAME')
    dbURL=os.environ.get('SPRING_DATASOURCE_URL')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@party-management-individual-postgresql:5432/party_management_individual'.format(dbUSER,dbPWD)

class ProductionConfig(Config):
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')