from extensions.extensions import db

class Faculty(db.Model):
    __tablename__ = 'faculty'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    faculty_code = db.Column(db.Text, nullable=False, unique=True)
    faculty_name = db.Column(db.Text, nullable=False)
    kafedras = db.relationship('Kafedra', backref='faculty', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'faculty_code': self.faculty_code,
            'faculty_name': self.faculty_name,
        }

class Kafedra(db.Model):
    __tablename__ = 'cafedras'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cafedra_code = db.Column(db.Text, nullable=False, unique=True)
    cafedra_name = db.Column(db.Text, nullable=False)

    faculty_code = db.Column(db.Text, db.ForeignKey('faculty.faculty_code'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'cafedra_code': self.cafedra_code,
            'cafedra_name': self.cafedra_name,
            'faculty_code': self.faculty_code,
            'faculty_name': self.faculty.faculty_name if self.faculty else None
        }