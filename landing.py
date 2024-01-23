# from datetime import datetime
#
# from flask_bcrypt import Bcrypt
# from flask import Flask, request, render_template, redirect, Blueprint, flash, url_for, session
# from flask_jsglue import JSGlue
#
# from flask_login import login_user, logout_user, current_user
#
# from app import db
#
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static/images'
#
# jsglue = JSGlue()
#
# bcrypt = Bcrypt()
#
# # ngambil class dari model
# # from models import category, Product, Users
#
# user = Blueprint(
#     "user", __name__, template_folder="templates", static_folder="static"
# )
#
#
# # # buat table
# @user.before_app_request
# def create_tables():
#     db.create_all()
#
#
# # untuk current time
# @user.context_processor
# def inject_current_datetime():
#     return dict(current_datetime=datetime.now())
#
#
# # ------------------------SEBELUM LOGIN------------------------------
#
# # awal page dibuka
# @user.route('/', methods=['POST', 'GET'])
# def home():
#     active_page = 'home'
#     if current_user.is_authenticated:
#         if current_user.role == '1':
#             return redirect(url_for('adm.dashboard'))
#         else:
#             flash("Anda sudah login. Anda tidak diperbolehkan mengakses halaman ini.", "warning")
#             return redirect(url_for('cust.dashboarduser'))
#     kategori = category.query.all()
#     pilihkategori = request.form.get('id_kategori', 'semua')
#     if pilihkategori == 'semua':
#         produk_ditemukan = Product.query.limit(4).all()
#     else:
#         produk_ditemukan = Product.query.filter_by(id_kategori=pilihkategori).limit(4).all()
#
#     return render_template('guest/index.html', pilihkategori=pilihkategori, prdk=produk_ditemukan,
#                            kategori=kategori, active_page=active_page)
#
#
# # halaman cari produk sesuai kategori produk (tidak perlu login)
# # @user.route('/productuser', methods=['POST'])
# # def cari_produk():
# #     active_page = 'productuser'
# #     if current_user.is_authenticated:
# #         if current_user.role == '1':
# #             return redirect(url_for('adm.dashboard'))
# #         else:
# #             flash("Anda sudah login. Anda tidak diperbolehkan mengakses halaman ini.", "warning")
# #             return redirect(url_for('cust.dashboarduser'))
# #     kategori = category.query.all()
# #
# #     if request.method == 'POST':
# #         kategori_terpilih = request.form.get('id_kategori', 'semua')
# #
# #         if kategori_terpilih == 'semua':
# #             produk_ditemukan = Product.query.all()
# #         else:
# #             produk_ditemukan = Product.query.filter_by(id_kategori=kategori_terpilih).all()
# #     else:
# #         # Jika bukan metode POST, tampilkan semua produk
# #         produk_ditemukan = Product.query.all()
# #
# #     return render_template('guest/produkuser.html', kategori_terpilih=kategori_terpilih, prdk=produk_ditemukan,
# #                            kategori=kategori, active_page=active_page)
# #
# #
# # # halaman produk (tidak perlu login)
# # @user.route('/productuser')
# # def productuser():
# #     active_page = 'productuser'
# #     if current_user.is_authenticated:
# #         if current_user.role == '1':
# #             return redirect(url_for('adm.dashboard'))
# #         else:
# #             flash("Anda sudah login. Anda tidak diperbolehkan mengakses halaman ini.", "warning")
# #             return redirect(url_for('cust.dashboarduser'))
# #     kategori = category.query.all()
# #     prdk = Product.query.all()
# #     return render_template('guest/produkuser.html', prdk=prdk, kategori=kategori, active_page=active_page)
# #
# #
# # @user.route('/detailprodukuser/<int:id_produk>', methods=['GET', 'POST'])
# # def detailproduknotlogin(id_produk):
# #     produk = Product.query.filter_by(id_produk=id_produk).first()
# #     if produk:
# #         return render_template('guest/detailproduk.html', produk=produk)
# #     return f"Produk dengan id ={id_produk} tidak ada brow "
# #
#
# # halaman register
# @user.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         if current_user.role == '1':
#             return redirect(url_for('adm.dashboard'))
#         else:
#             flash("Anda sudah login. Anda tidak diperbolehkan mengakses halaman ini.", "warning")
#             return redirect(url_for('cust.dashboarduser'))
#     if request.method == 'POST':
#         email = request.form['email']
#         username = request.form['username']
#         password = request.form['password']
#         fullname = request.form['fullname']
#         usia = request.form['usia']
#         alamat = request.form['alamat']
#         role_id = request.form['role_id']
#         notelp = request.form['notelp']
#
#         if len(username) < 5:
#             flash('Username harus lebih dari 5 karakter.', 'danger')
#             return redirect(url_for('user.register'))
#
#         if len(password) < 5:
#             flash('Password harus lebih dari 5 karakter.', 'danger')
#             return redirect(url_for('user.register'))
#
#         if len(usia) > 2:
#             flash('Usia anda sepertinya tidak masuk akal.', 'danger')
#             return redirect(url_for('user.register'))
#
#         # Cek apakah username sudah ada dalam basis data
#         existing_user = Users.query.filter_by(username=username).first()
#
#         if existing_user:
#             flash('Username ini sudah digunakan. Silakan pilih username lain.', 'danger')
#             return redirect(url_for('user.register'))
#         password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')
#
#         user = Users(email=email, username=username, password=password_hashed, fullname=fullname, usia=usia,
#                      alamat=alamat, role_id=role_id, notelp=notelp)
#
#         db.session.add(user)
#         db.session.commit()
#
#         flash('Akun berhasil dibuat. Anda dapat login sekarang.', 'success')
#         return redirect(url_for('user.login'))
#     return render_template('guest/register.html')
#
#
# # login semua role(logika user admin ada di dalam fungsi)
# @user.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         if current_user.role == '1':
#             return redirect(url_for('adm.dashboard'))
#         else:
#             flash("Anda sudah login. Anda tidak diperbolehkan mengakses halaman ini.", "warning")
#             return redirect(url_for('cust.dashboarduser'))
#     if request.method == 'POST':
#         username_atau_email = request.form['username_atau_email']
#         password = request.form['password']
#
#         user = Users.query.filter(
#             (Users.username == username_atau_email) | (Users.email == username_atau_email)).first()
#
#         if user and bcrypt.check_password_hash(user.password, password):
#             login_user(user)
#             flash('Login berhasil!', 'success')
#             if user.role.role_name == 'admin':
#                 return redirect(url_for('adm.dashboard'))
#             else:
#                 return redirect(url_for('cust.dashboarduser'))
#         else:
#             flash('Login gagal. Periksa kembali username dan kata sandi Anda.', 'danger')
#
#     return render_template('guest/login.html')
#
#
# @user.route('/logout')
# def logout():
#     if 'cart' in session:
#         cart_items = session['cart']
#         for cart in cart_items:
#             id_produk = cart['id_produk']
#             quantity = cart['quantity']
#             product = Product.query.get(id_produk)
#             if product:
#                 product.stok += quantity
#                 db.session.commit()
#         del session['cart']
#     logout_user()
#     flash('Berhasil Logout!', 'success')
#     return redirect(url_for("user.home"))
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
