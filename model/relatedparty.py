from extensions import db

class RelatedParty(db.Model):
    __tablename__ = 'relatedparty'

    id_tech = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey("individual.id"), nullable=False)

    id = db.Column(db.String(),  nullable=False)
    href= db.Column(db.String(), nullable=True)
    name= db.Column(db.String(), nullable=True)
    role= db.Column(db.String(), nullable=True)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()