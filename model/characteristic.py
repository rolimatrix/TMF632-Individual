from extensions import db

class Characterstic(db.Model):
    __tablename__ = 'characteristic'

    id = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey("individual.id"), nullable=False)

    name = db.Column(db.String(), nullable=False)
    valueType = db.Column(db.String(), nullable=True)
    value = db.Column(db.String(), nullable=False)

    baseType = db.Column(db.String(), nullable=True, default='PartyChar')
    schemaLocation = db.Column(db.String(), nullable=True)
    type = db.Column(db.String(), nullable=True, default='PartyIndivChar')

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())


    @classmethod
    def get_by_id(cls, indiv_id):
        return cls.query.filter_by(id=indiv_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()