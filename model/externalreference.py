from extensions import db

class ExternalReference(db.Model):
    __tablename__ = 'externalreference'

    id = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey("individual.id"), nullable=False)

    externalReferenceType= db.Column(db.String(), nullable=True)
    name= db.Column(db.Integer, nullable=True)

    baseType = db.Column(db.Integer, nullable=True, default='ExternalReference')
    schemaLocation= db.Column(db.Integer, nullable=True)
    type= db.Column(db.Integer, nullable=True, default='ExternalReferencePartyIndic')

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())