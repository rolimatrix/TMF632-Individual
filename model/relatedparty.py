from extensions import db

class RelatedParty(db.Model):
    __tablename__ = 'relatedparty'

    id = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey("individual.id"), nullable=False)

    href= db.Column(db.String(), nullable=True)
    name= db.Column(db.Integer, nullable=True)
    role= db.Column(db.Integer, nullable=True)

    #baseType = db.Column(db.Integer, nullable=True, default='RelatedParty')
    #schemaLocation= db.Column(db.Integer, nullable=True)
    #type= db.Column(db.Integer, nullable=True, default='RelatedPartyIndiv')

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
