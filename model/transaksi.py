import uuid

from app import db
from model.user import Users


class TransaksiModel(db.Model):
    __tablename__ = "Transaksi"
    id_transaksi = db.Column(db.String, primary_key=True, nullable=False, unique=True, default=lambda: uuid.uuid4().hex)
    user_id = db.Column(db.String, db.ForeignKey('users.id'))
    user = db.relationship(Users, foreign_keys=user_id)
    total = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def __init__(self, user_id, date, total):
        self.user_id = user_id
        self.date = date
        self.total = total
