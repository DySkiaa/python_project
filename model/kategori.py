import uuid

from app import db


class KategoriModel(db.Model):
    __tablename__ = "kategori"
    id_kategori = db.Column(db.String, primary_key=True, nullable=False, unique=True, default=lambda: uuid.uuid4().hex)
    kategori = db.Column(db.String, nullable=False)

    def __init__(self, kategori):
        self.kategori = kategori