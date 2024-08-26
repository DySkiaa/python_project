import uuid

from app import db


class StatusPembayaranModel(db.Model):
    __tablename__ = "status_pembayaran"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    stats_pem_name = db.Column(db.String)

    def __init__(self, stats_pem_name):
        self.stats_pem_name = stats_pem_name
