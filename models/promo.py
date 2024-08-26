import uuid

from app import db


class PromoModel(db.Model):
    __tablename__ = "promo"
    id_promo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_promo = db.Column(db.String)
    diskon = db.Column(db.Integer)

    def __init__(self, nama_promo, diskon):
        self.nama_promo = nama_promo
        self.diskon = diskon