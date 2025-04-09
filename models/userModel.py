from sqlalchemy import ForeignKey
from extensions.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'sexsler'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    ata_adi = db.Column(db.String(100), nullable=False)
    fin_kod = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    faculty_code = db.Column(db.Integer, ForeignKey('faculty.faculty_code'))
    cafedra_code = db.Column(db.Text)
    vezife_id = db.Column(db.Integer)
    vezife_name = db.Column(db.Text)
    ishesabat = db.Column(db.Integer)
    role_code = db.Column(db.Integer, ForeignKey('roles.role_code'))
    faculty = db.relationship('Faculty', backref='faculties', lazy=True)
    role = db.relationship('Roles', backref='users', lazy=True)
    kafedras = db.relationship('Plan', backref='plan', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def user_detail(self):
        return {
            'id': self.id,
            'ad': self.ad,
            'soyad': self.soyad,
            'ata_adi': self.ata_adi,
            'fin_kod': self.fin_kod,
            'faculty_code': self.faculty_code,
            'faculty_name': self.faculty.faculty_name if self.faculty else None,
            'cafedra_code': self.cafedra_code,
            'vezife_id': self.vezife_id,
            'vezife_name': self.vezife_name,
            'ishesabat': self.ishesabat,
            'role_code': self.role_code
        }