from extensions.extensions import db

class Qiymetlendirme(db.Model):
    __tablename__ = 'qiymetlendirme'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seviyye_kodu = db.Column(db.Integer)
    seviyye_adi = db.Column(db.Integer)
    seviyye_izahi = db.Column(db.Text)


    def qiymetlendirme_details(self):
        return {
            'id': self.id,
            'seviyye_kodu': self.seviyye_kodu,
            'seviyye_adi': self.seviyye_adi,
            'seviyye_adi': self.seviyye_adi,
            'seviyye_izahi': self.seviyye_izahi
        }
