from sqlalchemy import ForeignKey
from extensions.extensions import db

class Pages(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_name = db.Column(db.Text, nullable=False)
    page_path = db.Column(db.Text, nullable=False)
    role_code = db.Column(db.Text, ForeignKey('roles.role_code'), nullable=False)

    def page_details(self):
        return {
            'id': self.id,
            'page_name': self.page_name,
            'page_path': self.page_path,
            'role_code': self.role_code
        }