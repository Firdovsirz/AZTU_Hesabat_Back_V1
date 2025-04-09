from extensions.extensions import db

class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_code = db.Column(db.Integer, nullable=False, unique=True)
    role_name = db.Column(db.Text, nullable=False, unique=True)
    