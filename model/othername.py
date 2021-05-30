from extensions import db

class OtherName(db.Model):
    __tablename__ = 'othername'
    id = db.Column(db.BigInteger, primary_key=True)
    fk_idIndiv = db.Column(db.BigInteger(), db.ForeignKey("individual.id"), nullable=False)

    aristocraticTitle = db.Column(db.String(), nullable=True)
    familyName= db.Column(db.String(), nullable=True)
    familyNamePrefix= db.Column(db.String(), nullable=True)
    formattedName= db.Column(db.String(), nullable=True)
    fullName= db.Column(db.String(), nullable=True)
    generation= db.Column(db.String(), nullable=True)
    givenName= db.Column(db.String(), nullable=True)
    legalName= db.Column(db.String(), nullable=True)
    middleName= db.Column(db.String(), nullable=True)
    preferredGivenName= db.Column(db.String(), nullable=True)
    title= db.Column(db.String(), nullable=True)

    validforendDateTime = db.Column(db.String(30), nullable=True)
    validforstartDateTime = db.Column(db.String(30), nullable=True)

    baseType = db.Column(db.Integer, nullable=True, default='OtherName')
    schemaLocation= db.Column(db.Integer, nullable=True)
    type= db.Column(db.Integer, nullable=True, default='OtherNamePartyIndiv')

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())