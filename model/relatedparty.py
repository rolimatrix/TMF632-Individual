# coding=utf-8
from extensions import db
import os

dbUSER=os.environ.get('SPRING_DATASOURCE_USERNAME')

class RelatedParty(db.Model):
    __tablename__ = 'relatedparty'
    __table_args__ = {'schema': dbUSER}

    id_tech = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey('individual.id')) #, nullable=False
    #individual = db.relationship("Individual", backref="relatedparty") #cascade="all, delete",

    id = db.Column(db.String(),  nullable=False)
    href= db.Column(db.String(), nullable=True)
    name= db.Column(db.String(), nullable=True)
    role= db.Column(db.String(), nullable=True)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def __init__(self,ordDict,individual):
        self.id = ordDict['id']
        self.href= ordDict.setdefault('href', None)
        self.name=ordDict.setdefault('name',None)
        self.role=ordDict.setdefault('role',None)
        self.individual=individual


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id_tech=id).first()