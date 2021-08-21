from extensions import db

class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey("individual.id"), nullable=False)

    comment = db.Column(db.String(), nullable=True)
    evaluatedLevel = db.Column(db.Integer, nullable=True)
    skillCode = db.Column(db.Integer, nullable=True)
    skillName = db.Column(db.Integer, nullable=True)

    validforendDateTime = db.Column(db.String(30), nullable=True)
    validforstartDateTime = db.Column(db.String(30), nullable=True)

    #baseType = db.Column(db.Integer, nullable=True, default='Skill')
    #schemaLocation= db.Column(db.Integer, nullable=True)
    #type= db.Column(db.Integer, nullable=True, default='SkillPartyIndiv')

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
