import uuid

from app import db
from models.kategori import KategoriModel
from models.promo import PromoModel
from models.status import StatusModel


class ProdukModel(db.Model):
    __tablename__ = "produk"

    id_produk = db.Column(db.String, primary_key=True, nullable=False, unique=True, default=lambda: uuid.uuid4().hex)
    nama_product = db.Column(db.String, nullable=False)
    deskripsi = db.Column(db.String)
    id_kategori = db.Column(db.String, db.ForeignKey('kategori.id_kategori'), nullable=False)
    kategori = db.relationship(KategoriModel, foreign_keys=id_kategori)
    harga = db.Column(db.Integer, nullable=False)
    gambar = db.Column(db.String)
    stok = db.Column(db.Integer, default=0)
    id_promo = db.Column(db.Integer, db.ForeignKey('promo.id_promo'))
    promo = db.relationship(PromoModel, foreign_keys=id_promo)
    id_status = db.Column(db.Integer, db.ForeignKey('status.id_status'))
    status = db.relationship(StatusModel, foreign_keys=id_status)
    selling = db.Column(db.Integer, default=0)

    def __init__(self, nama_product, deskripsi, id_kategori, harga, gambar, stok, id_promo, id_status, selling):
        self.nama_product = nama_product
        self.deskripsi = deskripsi
        self.id_kategori = id_kategori
        self.harga = harga
        self.gambar = gambar
        self.stok = stok
        self.id_promo = id_promo
        self.id_status = id_status
        self.selling = selling
