from extensions import db

class Characterstic(db.Model):
    __tablename__ = 'characteristic'

    id = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey("individual.id"), nullable=False)

    name = db.Column(db.String(), nullable=False)
    valueType = db.Column(db.String(), nullable=True)
    value = db.Column(db.String(), nullable=False)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()
