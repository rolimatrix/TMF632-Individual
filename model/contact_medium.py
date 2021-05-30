from extensions import db

class ContactMedium(db.Model):
    __tablename__ = 'contactmedium'

    id = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey("individual.id"), nullable=False)

    mediumType = db.Column(db.String(), nullable=True)
    preferred = db.Column(db.Boolean(), nullable=True)

    baseType = db.Column(db.String(), nullable=True, default='ContactMedium')
    schemaLocation = db.Column(db.String(), nullable=True)
    type = db.Column(db.String(), nullable=True, default = 'ContactMediumPartyIndiv')

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
    street2 = db.Column(db.String(), nullable=True)
    baseTypeMediChar = db.Column(db.String(), nullable=True)
    schemaLocationMediChar = db.Column(db.String(), nullable=True)
    typeMediChar = db.Column(db.String(), nullable=True)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_by_id(cls, fk_idIndiv):
        return cls.query.filter_by(id=fk_idIndiv).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()