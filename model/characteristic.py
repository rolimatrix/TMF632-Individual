# coding=utf-8
from extensions import db
import os
dbUSER=os.environ.get('SPRING_DATASOURCE_USERNAME')

class Characterstic(db.Model):
    __tablename__ ='characteristic'
    __table_args__ = {'schema': dbUSER}

    id = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey('individual.id'))
    #individual = db.relationship("Individual", backref="characteristic") #cascade="all, delete",

    name = db.Column(db.String(), nullable=False)
    valueType = db.Column(db.String(), nullable=True)
    value = db.Column(db.String(), nullable=False)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def __init__(self,ordDict,individual):
        self.name=ordDict['name']
        self.valueType=ordDict.setdefault('valueType',None)
        self.value=ordDict['value']
        self.individual=individual


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
