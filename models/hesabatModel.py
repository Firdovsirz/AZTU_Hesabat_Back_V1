from extensions.extensions import db

class Hesabat(db.Model):
    __tablename__ = 'yekun_hesabat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hesabat_ilinin_kodu = db.Column(db.TIMESTAMP, nullable=False)
    bolme_novu_id = db.Column(db.Integer, nullable=True)
    isin_sira_sayi = db.Column(db.Integer, nullable=False, unique=True)
    fealiyyet_novu_id = db.Column(db.Integer, nullable=False)
    fealiyyet_novu_adi = db.Column(db.Text, nullable=False)
    fin_kod = db.Column(db.String(10), nullable=False)
    icra_muddeti = db.Column(db.TIMESTAMP, nullable=False)
    fealiyyetin_neticesi = db.Column(db.LargeBinary)
    isin_gorulme_faizi = db.Column(db.Integer)
    teqdim_etme_tarixi = db.Column(db.TIMESTAMP)
    vaxt_tehlili = db.Column(db.Boolean)
    qeyd = db.Column(db.Text)

    def hesabat_details(self):
        return {
            'id': self.id,
            'hesabat_ilinin_kodu': self.hesabat_ilinin_kodu,
            'bolme_novu_id': self.bolme_novu_id,
            'isin_sira_sayi': self.isin_sira_sayi,
            'fealiyyet_novu_id': self.fealiyyet_novu_id,
            'fealiyyet_novu_adi': self.fealiyyet_novu_adi,
            'icra_muddeti': self.icra_muddeti,
            'fin_kod': self.fin_kod,
            'icra_muddeti': self.icra_muddeti,
            'fealiyyetin_neticesi': self.fealiyyetin_neticesi,
            'isin_gorulme_faizi': self.isin_gorulme_faizi,
            'teqdim_etme_tarixi': self.teqdim_etme_tarixi,
            'vaxt_tehlili': self.vaxt_tehlili,
            'qeyd': self.qeyd,
        }