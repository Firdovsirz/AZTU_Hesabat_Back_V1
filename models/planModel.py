from extensions.extensions import db

class Plan(db.Model):
    __tablename__ = 'is_plani'
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    hesabat_ilinin_kodu = db.Column(db.TIMESTAMP, nullable=False)
    bolme_novu_id = db.Column(db.Integer, nullable=False)
    isin_sira_sayi = db.Column(db.Integer, nullable=False)
    fealiyyet_novu_id = db.Column(db.Integer, nullable=False)
    fealiyyet_novu_adi = db.Column(db.Text, nullable=False)
    icra_muddeti = db.Column(db.TIMESTAMP, nullable=False)
    fin_kod = db.Column(db.String(10), db.ForeignKey('sexsler.fin_kod'))

    def plan_details(self):
        return {
            'id': self.id,
            'hesabat_ilinin_kodu': self.hesabat_ilinin_kodu,
            'bolme_novu_id': self.bolme_novu_id,
            'isin_sira_sayi': self.isin_sira_sayi,
            'fealiyyet_novu_id': self.fealiyyet_novu_id,
            'fealiyyet_novu_adi': self.fealiyyet_novu_adi,
            'icra_muddeti': self.icra_muddeti,
            'fin_kod': self.fin_kod
        }