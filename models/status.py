from app import db


class StatusModel(db.Model):
    __tablename__ = "status"
    id_status = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_status = db.Column(db.String, nullable=False)

    def __init__(self, nama_status):
        self.nama_status = nama_status
