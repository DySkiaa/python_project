import uuid

from app import db
from models.produk import ProdukModel
from models.transaksi import TransaksiModel


class TransaksiDetailModel(db.Model):
    __tablename__ = "detail_transaksi"
    id_detailtransaksi = db.Column(db.String, primary_key=True, nullable=False, unique=True,
                                   default=lambda: uuid.uuid4().hex)
    id_transaksi = db.Column(db.String, db.ForeignKey('Transaksi.id_transaksi'))
    transaksi = db.relationship(TransaksiModel, foreign_keys=id_transaksi)
    id_produk = db.Column(db.String, db.ForeignKey('produk.id_produk'))
    produk = db.relationship(ProdukModel, foreign_keys=id_produk)
    quantity = db.Column(db.Integer)
    subtotal = db.Column(db.Integer)

    def __init__(self, id_transaksi, id_produk, quantity, subtotal):
        self.id_transaksi = id_transaksi
        self.id_produk = id_produk
        self.quantity = quantity
        self.subtotal = subtotal
