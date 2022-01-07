# coding=utf-8
from extensions import db
import os
dbUSER=os.environ.get('SPRING_DATASOURCE_USERNAME')

class ContactMedium(db.Model):
    __tablename__ = 'contactmedium'
    __table_args__ = {'schema': dbUSER}

    id = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey('individual.id')) #, nullable=False

    #individual = db.relationship("Individual", backref="contactmedium") #cascade="all, delete",

    mediumType = db.Column(db.String(), nullable=False)
    preferred = db.Column(db.Boolean(), nullable=True)
    mediumVerified= db.Column(db.Boolean(), nullable=True, default=False)

    endDateTime =  db.Column(db.String(), nullable=True)
    startDateTime = db.Column(db.String(), nullable=True)

    city = db.Column(db.String(), nullable=True)
    contactType = db.Column(db.String(), nullable=True)
    country = db.Column(db.String(), nullable=True)
    emailAddress = db.Column(db.String(), nullable=True)
    faxNumber = db.Column(db.String(), nullable=True)
    phoneNumber = db.Column(db.String(), nullable=True)
    postCode = db.Column(db.String(), nullable=True)
    socialNetworkId = db.Column(db.String(), nullable=True)
    stateOrProvince= db.Column(db.String(), nullable=True)
    street1 = db.Column(db.String(), nullable=True)
    houseNumber=db.Column(db.String(), nullable=True)
    houseNumberAppendix=db.Column(db.String(), nullable=True)
    street2 = db.Column(db.String(), nullable=True)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def __init__(self,ordDict, individual):

        self.mediumType = ordDict['mediumType']
        self.preferred = ordDict.setdefault('preferred',False)
        self.mediumVerified = ordDict.setdefault('mediumVerified',False)
        self.endDateTime = ordDict.setdefault('endDateTime',None)
        self.startDateTime = ordDict.setdefault('startDateTime',None)
        self.city = ordDict.setdefault('city',None)
        self.contactType = ordDict.setdefault('contactType',None)
        self.country = ordDict.setdefault('country',None)
        self.emailAddress = ordDict.setdefault('emailAddress',None)
        self.faxNumber = ordDict.setdefault('faxNumber',None)
        self.phoneNumber = ordDict.setdefault('phoneNumber',None)
        self.postCode = ordDict.setdefault('postCode',None)
        self.socialNetworkId = ordDict.setdefault('socialNetworkId',None)
        self.stateOrProvince = ordDict.setdefault('stateOrProvince',None)
        self.street1 = ordDict.setdefault('street1',None)
        self.houseNumber = ordDict.setdefault('houseNumber',None)
        self.houseNumberAppendix = ordDict.setdefault('houseNumberAppendix',None)
        self.street2 = ordDict.setdefault('street2',None)
        self.individual = individual



