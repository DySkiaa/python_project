import uuid

from app import db
from models.status_pemabayaran import StatusPembayaranModel
from models.user import Users


class TransaksiModel(db.Model):
    __tablename__ = "Transaksi"
    id_transaksi = db.Column(db.String, primary_key=True, nullable=False, unique=True, default=lambda: uuid.uuid4().hex)
    user_id = db.Column(db.String, db.ForeignKey('users.id'))
    user = db.relationship(Users, foreign_keys=user_id)
    total = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    status_pembayaran = db.Column(db.Integer, db.ForeignKey('status_pembayaran.id'), default=1)
    stat_pem = db.relationship(StatusPembayaranModel, foreign_keys=status_pembayaran)
    picture = db.Column(db.String)

    def __init__(self, user_id, date, total, status_pembayaran, picture):
        self.user_id = user_id
        self.date = date
        self.total = total
        self.status_pembayaran = status_pembayaran
        self.picture = picture
