# coding=utf-8
from extensions import db
import os
dbUSER=os.environ.get('SPRING_DATASOURCE_USERNAME')

class Individual(db.Model):
    __tablename__ = 'individual'
    #__table_args__ = {'schema': dbUSER}

    id = db.Column(db.BigInteger,primary_key=True, autoincrement=True)
    status = db.Column(db.String(), nullable=True, default="initialized")
    aristocraticTitle = db.Column(db.String(), nullable=True)
    birthDate = db.Column(db.String(), nullable=True)
    countryOfBirth = db.Column(db.String(), nullable=True)
    deathDate= db.Column(db.String(), nullable=True)
    familyName = db.Column(db.String(), nullable=False)
    familyNamePrefix= db.Column(db.String(), nullable=True)
    formattedName = db.Column(db.String(), nullable=True)
    fullName = db.Column(db.String(), nullable=True)
    gender = db.Column(db.String(), nullable=True)
    generation = db.Column(db.String(), nullable=True)
    givenName = db.Column(db.String(), nullable=False)
    legalName = db.Column(db.String(), nullable=True)
    location = db.Column(db.String(), nullable=True)
    maritalStatus = db.Column(db.String(), nullable=True)
    middleName = db.Column(db.String(), nullable=True)
    nationality = db.Column(db.String(), nullable=True)
    placeOfBirth = db.Column(db.String(), nullable=True)
    preferredGivenName = db.Column(db.String(), nullable=True)
    title = db.Column(db.String(), nullable=True)

    contactmedium = db.relationship("ContactMedium", cascade="all, delete",backref="individual")
    characteristic = db.relationship("Characterstic", cascade="all, delete",backref="individual")
    relatedparty = db.relationship("RelatedParty", cascade="all, delete", backref="individual")

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())


    @classmethod
    def get_by_id(cls, indiv_id):
        return cls.query.filter_by(id=indiv_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()