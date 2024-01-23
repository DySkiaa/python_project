import hashlib

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt

# db = SQLAlchemy()

# bcrypt = Bcrypt()


# membuat product
# class Product(db.Model):
#     __tablename__ = "produk"
#     id_produk = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     nama_product = db.Column(db.String, nullable=False)
#     deskripsi = db.Column(db.String)
#     id_kategori = db.Column(db.Integer, db.ForeignKey('kategori.id_kategori'), nullable=False)
#     harga = db.Column(db.Integer, nullable=False)
#     gambar = db.Column(db.String)
#     stok = db.Column(db.Integer)
#     id_promo = db.Column(db.Integer, db.ForeignKey('promo.id_promo'))
#
#     Promo = db.relationship('Promo', backref='Product')
#
#     category = db.relationship('category', backref='products')
#
#     def __init__(self, nama_product, deskripsi, id_kategori, harga, gambar, stok, id_promo):
#         self.nama_product = nama_product
#         self.deskripsi = deskripsi
#         self.id_kategori = id_kategori
#         self.harga = harga
#         self.gambar = gambar
#         self.stok = stok
#         self.id_promo = id_promo

    # def generate_id(self):
    #     # You can use some unique information from the record to generate a hash
    #     hash_input = f'{self.nama_product}-{self.id_kategori}-{self.harga}-{self.deskripsi}'
    #     return hashlib.sha256(hash_input.encode()).hexdigest()


# class category(db.Model):
#     __tablename__ = "kategori"
#     id_kategori = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     kategori = db.Column(db.String, nullable=False)
#
#     def __init__(self, kategori):
#         self.kategori = kategori


# Create user model
# class Users(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String)
#     username = db.Column(db.String(250), unique=True,
#                          nullable=False)
#     password = db.Column(db.String(250),
#                          nullable=False)
#     fullname = db.Column(db.String)
#     usia = db.Column(db.Integer)
#     alamat = db.Column(db.String)
#     role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
#     notelp = db.Column(db.String)
#
#     role = db.relationship('Role', backref='users')
#
#     def __int__(self, email, username, password, fullname, usia, alamat, role_id, notelp):
#         self.email = email
#         self.username = username
#         self.password = Bcrypt.generate_password_hash(password).decode('utf-8')
#         self.fullname = fullname
#         self.usia = usia
#         self.alamat = alamat
#         self.role_id = role_id
#         self.notelp = notelp


# class Role(db.Model):
#     __tablename__ = "role"
#     role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     role_name = db.Column(db.String(80), unique=True, nullable=False)
#
#     def __init__(self, role_name):
#         self.role_name = role_name


# Tabel Transaksi (Transaction)
# class Transaksi(db.Model):
#     __tablename__ = "transaksi"
#     id_transaksi = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     total = db.Column(db.Integer)
#     date = db.Column(db.DateTime)
#
#     user = db.relationship(Users, backref='Transaksi')
#     # Relasi dengan Detail Transaksi
#     details = db.relationship('DetailTransaksi', backref='Transaksi', lazy=True)
#
#     def __init__(self, user_id, date, total):
#         self.user_id = user_id
#         self.date = date
#         self.total = total


# Tabel Detail Transaksi (TransactionDetail)
# class DetailTransaksi(db.Model):
#     __tablename__ = "detail_transaksi"
#     id_detailtransaksi = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     id_transaksi = db.Column(db.Integer, db.ForeignKey('Transaksi.id_transaksi'))
#     id_produk = db.Column(db.Integer, db.ForeignKey('produk.id_produk'))
#     quantity = db.Column(db.Integer)
#     subtotal = db.Column(db.Integer)
#
#     transaksi = db.relationship('Transaksi', backref='DetailTransaksi')
#     Product = db.relationship('Product', primaryjoin='DetailTransaksi.id_produk == Product.id_produk',
#                               backref='DetailTransaksi')
#
#     def __init__(self, id_transaksi, id_produk, quantity, subtotal):
#         self.id_transaksi = id_transaksi
#         self.id_produk = id_produk
#         self.quantity = quantity
#         self.subtotal = subtotal
#
#
# class Promo(db.Model):
#     __tablename__ = "promo"
#     id_promo = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     nama_promo = db.Column(db.String)
#     diskon = db.Column(db.Integer)
#
#     def __init__(self, nama_promo, diskon):
#         self.nama_promo = nama_promo
#         self.diskon = diskon
