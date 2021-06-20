from extensions import db
class Individual(db.Model):
    __tablename__ = 'individual'

    id = db.Column(db.BigInteger, primary_key=True)
    status = db.Column(db.String(), nullable=False, default="initialized")
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

    contactmedium = db.relationship('ContactMedium', cascade="all, delete",backref='individual')
    characteristic = db.relationship('Characterstic', cascade="all, delete",backref='individual')
    othername = db.relationship('OtherName', cascade="all, delete", backref='individual')
    relatedparty = db.relationship('RelatedParty', cascade="all, delete", backref='individual')
    skill = db.relationship('Skill', cascade="all, delete", backref='individual')
    externalreference = db.relationship('ExternalReference', cascade="all, delete", backref='individual')

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