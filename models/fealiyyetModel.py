from extensions.extensions import db

class Fealiyyet(db.Model):
    __tablename__ = 'fealiyyet_novleri'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fealiyyet_novu_id = db.Column(db.Integer, nullable=False)
    fealiyyet_novu_mezmunu = db.Column(db.Text, nullable=False)

    def fealiyyet_details(self):
        return {
            'id': self.id,
            'fealiyyet_novu_id': self.fealiyyet_novu_id,
            'fealiyyet_novu_mezmunu': self.fealiyyet_novu_mezmunu
        }