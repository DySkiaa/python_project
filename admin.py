# from datetime import datetime
#
# from flask import Blueprint, flash, redirect, url_for, render_template, request, Flask
# from flask_login import login_required, current_user, logout_user
#
# from app import db
# # from models import Transaksi, DetailTransaksi, Users, category, Product, bcrypt, Promo
#
# adm = Blueprint("adm", __name__, template_folder="templates", static_folder="static"
#                 )
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static/images'
#
#
# # # buat table
# @adm.before_app_request
# def create_tables():
#     db.create_all()
#
#
# # untuk current time
# @adm.context_processor
# def inject_current_datetime():
#     return dict(current_datetime=datetime.now())
#
#
# @adm.routes_admin('/page_home')
# @login_required
# def dashboard():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#
#     breadcrumb_data = ['Dashboard', 'Home']  # Data breadcrumb
#     transaksi = Transaksi.query.all()
#     produk = Product.query.all()
#     cust = Users.query.filter_by(role_id=2).all()
#
#     cust = len(cust)
#     produk = len(produk)
#     total = sum(transaksi.total for transaksi in transaksi)
#     transaksi = len(transaksi)
#     return render_template('admin/dashboard.html', cust=cust, produk=produk, total=total,
#                            breadcrumb_data=breadcrumb_data, transaksi=transaksi)
#
#
# # halaman detail akun admin
# @adm.routes_admin('/detailakun/<int:id>', methods=['GET', 'POST'])
# @login_required
# def detailakun(id):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     user = Users.query.get(id)
#     breadcrumb_data = ['Dashboard', 'Detail Akun']  # Data breadcrumb
#     if user and user == current_user:
#         new_fullname = None
#         new_usia = None
#         new_alamat = None
#         new_notelp = None
#
#         if request.method == 'POST':
#             new_fullname = request.form.get('new_fullname')
#             new_usia = request.form.get('new_usia')
#             new_alamat = request.form.get('new_alamat')
#             new_notelp = request.form.get('new_notelp')
#
#             user.fullname = new_fullname
#             user.usia = new_usia
#             user.alamat = new_alamat
#             user.notelp = new_notelp
#             db.session.commit()
#             flash('Profil berhasil diperbarui.', 'success')
#             return redirect(url_for('adm.dashboard', id=id))
#
#         return render_template('admin/customer/detailadmin.html', user=user, new_usia=new_usia, new_alamat=new_alamat,
#                                new_fullname=new_fullname, new_notelp=new_notelp, breadcrumb_data=breadcrumb_data)
#
#
# # register akun admin
# @adm.routes_admin('/addadmin', methods=['GET', 'POST'])
# @login_required
# def addadmin():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Dashboard', 'Tambah Akun Admin']  # Data breadcrumb
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
#             return redirect(url_for('adm.addadmin'))
#
#         if len(password) < 5:
#             flash('Password harus lebih dari 5 karakter.', 'danger')
#             return redirect(url_for('adm.addadmin'))
#
#         if len(usia) > 2:
#             flash('Usia anda sepertinya tidak masuk akal.', 'danger')
#             return redirect(url_for('adm.addadmin'))
#
#         # Cek apakah username sudah ada dalam basis data
#         existing_user = Users.query.filter_by(username=username).first()
#
#         if existing_user:
#             flash('Username ini sudah digunakan. Silakan pilih username lain.', 'danger')
#             return redirect(url_for('adm.addadmin'))
#         password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')
#
#         user = Users(email=email, username=username, password=password_hashed, fullname=fullname, usia=usia,
#                      alamat=alamat,
#                      role_id=role_id, notelp=notelp)
#
#         db.session.add(user)
#         db.session.commit()
#
#         flash('Akun berhasil dibuat.', 'success')
#         return redirect(url_for('adm.dashboard'))
#     return render_template('admin/addadmin.html', breadcrumb_data=breadcrumb_data)
#
#
# # ganti password admin
# @adm.routes_admin('/change_password', methods=['GET', 'POST'])
# @login_required
# def gantipassword():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#
#     breadcrumb_data = ['Dashboard', 'Ganti Password']  # Data breadcrumb
#     if request.method == 'POST':
#         old_password = request.form['old_password']
#         new_password = request.form['new_password']
#         confirm_password = request.form['confirm_password']
#
#         if bcrypt.check_password_hash(current_user.password, old_password):
#             if new_password == confirm_password:
#                 hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
#                 current_user.password = hashed_password
#                 db.session.commit()
#                 flash('Kata sandi telah diganti.', 'success')
#                 return redirect(url_for('adm.dashboard'))
#             elif new_password == old_password:
#                 flash('Kata sandi baru harus berbeda dari kata sandi lama.', 'warning')
#             else:
#                 flash('Konfirmasi kata sandi tidak cocok.', 'warning')
#         else:
#             flash('Kata sandi lama salah.', 'warning')
#
#     return render_template('admin/change_password.html', breadcrumb_data=breadcrumb_data)


# halaman crud produk (hanya admin)
# @adm.routes_admin('/page_product')
# @login_required
# def product():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Dashboard', 'Produk']  # Data breadcrumb
#     prdk = Product.query.all()
#     return render_template('admin/index.html', prdk=prdk, breadcrumb_data=breadcrumb_data)
#
#
# # halaman tambah produk (hanya admin)
# @adm.routes_admin('/tambahproduk', methods=['GET', 'POST'])
# @login_required
# def tambahproduk():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#
#     kategori = category.query.all()
#     breadcrumb_data = ['Produk', 'Tambah Produk']  # Data breadcrumb
#     if request.method == 'GET':
#         return render_template('admin/tambahproduk.html', breadcrumb_data=breadcrumb_data, kategori=kategori)
#     if request.method == 'POST':
#         nama_product = request.form['nama_product']
#         deskripsi = request.form['deskripsi']
#         id_kategori = request.form['id_kategori']
#         harga = float(request.form['harga'])
#         gambar = request.form['gambar']
#         stok = int(request.form['stok'])
#         id_promo = request.form['id_promo']
#
#         if harga < 0 or stok < 0:
#             flash('Harga dan stok tidak boleh kurang dari 0.', 'warning')
#             return redirect(url_for('adm.tambahproduk'))
#
#         produk = Product(nama_product=nama_product, deskripsi=deskripsi, id_kategori=id_kategori, harga=harga,
#                          gambar=gambar, stok=stok, id_promo=id_promo)
#
#         db.session.add(produk)
#         db.session.commit()
#         flash('Data Produk Berhasil Di Input!', 'success')
#         return redirect(url_for('adm.product'))
#
#     return render_template('admin/tambahproduk.html', breadcrumb_data=breadcrumb_data)
#
#
# # halaman edit produk(hanya admin)
# @adm.routes_admin('/editproduk/<int:id_produk>', methods=['GET', 'POST'])
# @login_required
# def editproduk(id_produk):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Produk', 'Edit Produk']  # Data breadcrumb
#     produk = Product.query.filter_by(id_produk=id_produk).first()
#     kategori_option = category.query.all()
#
#     if request.method == 'POST':
#
#         nama_product = request.form['nama_product']
#         deskripsi = request.form['deskripsi']
#         id_kategori = request.form['id_kategori']
#         harga = float(request.form['harga'])
#         gambar = request.form['gambar']
#
#         if harga < 0:
#             flash('Harga tidak boleh kurang dari 0.', 'warning')
#             return redirect(url_for('adm.editproduk', id_produk=id_produk))
#         # Cek apakah kolom gambar diisi atau tidak
#         if not gambar:
#             # Jika tidak diisi, gunakan gambar saat ini
#             gambar = produk.gambar
#
#         produk.nama_product = nama_product
#         produk.deskripsi = deskripsi
#         produk.id_kategori = id_kategori
#         produk.harga = harga
#         produk.gambar = gambar
#
#         db.session.commit()
#         flash('Produk Berhasil Di Edit!', 'success')
#         return redirect(url_for('adm.product'))
#
#         return f"Produk dengan ID = {id_produk} tersebut tidak ada"
#
#     return render_template('admin/editproduk.html', breadcrumb_data=breadcrumb_data, produk=produk,
#                            kategori_option=kategori_option)
#
#
# # tambah stok produk
# @adm.routes_admin('/tambahstok/<int:id_produk>', methods=['GET', 'POST'])
# @login_required
# def tambahstok(id_produk):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#
#     breadcrumb_data = ['Produk', 'Tambah Stok']  # Data breadcrumb
#
#     produk = Product.query.get(id_produk)
#
#     if not produk:
#         return "Produk dengan ID tersebut tidak ditemukan"
#
#     if request.method == 'POST':
#         stok_tambahan = int(request.form['stok'])
#
#         if stok_tambahan < 0:
#             flash('Jumlah stok yang diinput tidak valid.', 'warning')
#         else:
#             stok_baru = stok_tambahan
#             produk.stok = stok_baru
#             db.session.commit()
#             flash('Stok Produk Berhasil Ditambah!', 'success')
#             return redirect(url_for('adm.product'))
#
#     return render_template('admin/tambahstok.html', produk=produk, breadcrumb_data=breadcrumb_data)
#
#
# # halaman detail (produk)
# @adm.routes_admin('/detailproduk/<int:id_produk>')
# @login_required
# def detailproduk(id_produk):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     produk = Product.query.filter_by(id_produk=id_produk).first()
#     breadcrumb_data = ['Produk', 'Detail Produk']  # Data breadcrumb
#     if produk:
#         return render_template('admin/detailproduk.html', produk=produk, breadcrumb_data=breadcrumb_data)
#     return f"Produk dengan id ={id_produk} tidak ada brow "
#
#
# # delete produk
# @adm.routes_admin('/deleteprdk/<int:id_produk>', methods=['GET', 'POST'])
# @login_required
# def deleteprdk(id_produk):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     produk = Product.query.get(id_produk)
#     breadcrumb_data = ['Produk', 'Hapus Produk']  # Data breadcrumb
#     if request.method == 'POST':
#         if produk:
#             db.session.delete(produk)
#             db.session.commit()
#             flash('Produk  Berhasil Di Hapus!', 'success')
#             return redirect(url_for('adm.product'))
#
#     return render_template('deletepages.html', produk=produk, breadcrumb_data=breadcrumb_data)


# # halaman kategori (hanya admin)
# @adm.routes_admin('/page_kategori')
# @login_required
# def kategori():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Dashboard', 'Kategori']  # Data breadcrumb
#     ktgr = category.query.all()
#     return render_template('admin/kategori/index.html', ktgr=ktgr, breadcrumb_data=breadcrumb_data)
#
#
# # halaman tambah kategori
# @adm.routes_admin('/tambahkategori', methods=['GET', 'POST'])
# @login_required
# def tambahkategori():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Kategori', 'Tambah kategori']  # Data breadcrumb
#     if request.method == 'GET':
#         return render_template('admin/kategori/tambahkategori.html', breadcrumb_data=breadcrumb_data)
#     if request.method == 'POST':
#         kategori = request.form['kategori']
#         kategori = category(kategori=kategori)
#         db.session.add(kategori)
#         db.session.commit()
#         flash('Kategori Berhasil Di Tambahkan!', 'success')
#         return redirect(url_for('adm.kategori'))
#     return render_template('admin/kategori/tambahkategori.html', breadcrumb_data=breadcrumb_data)
#
#
# # halaman edit kategori
# @adm.routes_admin('/editktgr/<int:id_kategori>', methods=['GET', 'POST'])
# @login_required
# def editktgr(id_kategori):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     kategori = category.query.get(id_kategori)
#     breadcrumb_data = ['Kategori', 'Edit kategori']  # Data breadcrumb
#     if request.method == 'POST':
#         if kategori:
#             # Update data kategori dengan data baru dari formulir
#             kategori.kategori = request.form['kategori']
#
#             db.session.commit()
#             flash('Kategori Berhasil Di Edit!', 'success')
#             return redirect(url_for('adm.kategori'))
#         return f"Kategori dengan ID = {id_kategori} tersebut tidak ada"
#
#     return render_template('admin/kategori/editktgr.html', kategori=kategori, breadcrumb_data=breadcrumb_data)
#
#
# # halaman delet kategori
# @adm.routes_admin("/deletektgr/<int:id_kategori>", methods=["GET", "POST"])
# @login_required
# def deletektgr(id_kategori):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     kategori = category.query.filter_by(id_kategori=id_kategori).first()
#     breadcrumb_data = ['Kategori', 'Hapus Kategori']  # Data breadcrumb
#     if request.method == 'POST':
#         if kategori:
#             db.session.delete(kategori)
#             db.session.commit()
#             flash('Kategori  Berhasil Di Hapus!', 'success')
#             return redirect(url_for('adm.kategori'))
#
#     return render_template('deletepages.html', kategori=kategori, breadcrumb_data=breadcrumb_data)


# @adm.routes_admin('/page_promo')
# @login_required
# def promo():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Dashboard', 'Promo']  # Data breadcrumb
#     promo = Promo.query.all()
#
#     return render_template('admin/promo/index.html', breadcrumb_data=breadcrumb_data, promo=promo)
#
#
# @adm.routes_admin('/buatpromo', methods=['POST', 'GET'])
# @login_required
# def buatpromo():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Promo', 'Buat Promo']  # Data breadcrumb
#     if request.method == 'GET':
#         return render_template('admin/promo/buatpromo.html', breadcrumb_data=breadcrumb_data)
#     if request.method == 'POST':
#         nama_promo = request.form['nama_promo']
#         diskon = request.form['diskon']
#         promo = Promo(nama_promo=nama_promo, diskon=diskon)
#         db.session.add(promo)
#         db.session.commit()
#         flash('Kategori Berhasil Di Tambahkan!', 'success')
#         return redirect(url_for('adm.promo'))
#
#     return render_template('admin/promo/buatpromo.html', breadcrumb_data=breadcrumb_data)
#
# @adm.routes_admin('/editpromo/<int:id_promo>', methods=['GET', 'POST'])
# @login_required
# def editpromo(id_promo):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     promo = Promo.query.get(id_promo)
#     breadcrumb_data = ['Promo', 'Edit Promo']  # Data breadcrumb
#     if request.method == 'POST':
#         if promo:
#             # Update data kategori dengan data baru dari formulir
#             promo.nama_promo = request.form['nama_promo']
#             promo.diskon = request.form['diskon']
#
#             db.session.commit()
#             flash('Promo Berhasil Di Edit!', 'success')
#             return redirect(url_for('adm.promo'))
#         return f"Kategori dengan ID = {id_promo} tersebut tidak ada"
#
#     return render_template('admin/promo/editpromo.html', promo=promo, breadcrumb_data=breadcrumb_data)
#
# @adm.routes_admin('/deletepromo/<int:id_promo>', methods=['POST', 'GET'])
# @login_required
# def deletepromo(id_promo):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     promo = Promo.query.filter_by(id_promo=id_promo).first()
#     breadcrumb_data = ['Promo', 'Hapus Promo']  # Data breadcrumb
#     if request.method == 'POST':
#         if promo:
#             db.session.delete(promo)
#             db.session.commit()
#             flash('Promo  Berhasil Di Hapus!', 'success')
#             return redirect(url_for('adm.promo'))
#
#     return render_template('deletepages.html', promo=promo, breadcrumb_data=breadcrumb_data)
#
# @adm.routes_admin('/page_masukanpromo')
# @login_required
# def tambahpromo():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Promo', 'Tambah Promo']  # Data breadcrumb
#     prdk = Product.query.all()
#     # promo = Promo.query.all()
#
#     return render_template('admin/promo/index.html', produk=prdk, breadcrumb_data=breadcrumb_data)
#
#
# @adm.routes_admin('/tambahpromoproduk/<int:id_produk>', methods=['POST', 'GET'])
# @login_required
# def tambahpromoproduk(id_produk):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Promo', 'Tambah Promo Produk']  # Data breadcrumb
#     promo = Promo.query.all()
#     produk = Product.query.get(id_produk)
#
#     if request.method == 'GET':
#         return render_template('admin/promo/tambahpromo.html', promo=promo, breadcrumb_data=breadcrumb_data,
#                                kategori=kategori)
#     if request.method == 'POST':
#         id_promo = int(request.form['id_promo'])
#         produk.id_promo = id_promo
#         db.session.commit()
#
#         flash('Promo Produk Berhasil Ditambah!', 'success')
#         return redirect(url_for('adm.tambahpromo'))
#
#
# @adm.routes_admin('/cabutpromo/<int:id_produk>', methods=['POST', 'GET'])
# @login_required
# def cabutpromo(id_produk):
#     produk = Product.query.get(id_produk)
#
#     if produk:
#         produk.id_promo = None
#         db.session.commit()
#         flash('Promo telah dicabut dari produk.', 'success')
#     else:
#         flash('Produk tidak ditemukan.', 'warning')
#
#     return redirect(url_for('adm.tambahpromo'))


# # halaman list customer/user yang terdaftar
# @adm.routes_admin('/page_customer')
# @login_required
# def customer():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Dashboard', 'Customer']  # Data breadcrumb
#     user = Users.query.filter_by(role_id='2').all()
#     return render_template('admin/customer/index.html', user=user, breadcrumb_data=breadcrumb_data)
#
#
# # halaman transaksi yang dicari sesuai dari user_id
# @adm.routes_admin('/riwayat_transaksi/<int:user_id>')
# @login_required
# def riwayat(user_id):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['Customer', 'Transaksi']  # Data breadcrumb
#     riwayattransaksi = Transaksi.query.filter_by(user_id=user_id).all()
#     transaksi = Transaksi.query.filter_by(user_id=user_id).first()
#     user = Users.query.filter_by(id=user_id).first()
#     return render_template('admin/transaksi/riwayat.html', user=user, breadcrumb_data=breadcrumb_data, riwayattransaksi=riwayattransaksi, transaksi=transaksi)
#
#
# # halaman transaksi
# @adm.routes_admin('/page_transaksi')
# @login_required
# def transaksi():
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     breadcrumb_data = ['dashboard', 'Transaksi']  # Data breadcrumb
#     transaksi = Transaksi.query.all()
#     return render_template('admin/transaksi/index.html', transaksi=transaksi, breadcrumb_data=breadcrumb_data)
#
#
# # halaman detail transaksi
# @adm.routes_admin('/detailtransaksi/<int:id_transaksi>', methods=['POST', 'GET'])
# @login_required
# def transaksidetail(id_transaksi):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#
#     breadcrumb_data = ['Transaksi', 'Detail Transaksi']  # Data breadcrumb
#     transaksi = Transaksi.query.filter_by(id_transaksi=id_transaksi).first()
#     detail = DetailTransaksi.query.filter_by(id_transaksi=id_transaksi).all()
#     if detail:
#         return render_template('admin/transaksi/detailtransaksi.html', detail=detail, transaksi=transaksi,
#                                breadcrumb_data=breadcrumb_data)
#     return f"Produk dengan id ={id_transaksi} tidak ada brow "
#
#
# @adm.routes_admin('/cetakpdf/<int:id_transaksi>')
# @login_required
# def cetakpdf(id_transaksi):
#     if current_user.role.role_name != 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('cust.dashboarduser'))
#     transaksi = Transaksi.query.filter_by(id_transaksi=id_transaksi).first()
#     detail = DetailTransaksi.query.filter_by(id_transaksi=id_transaksi).all()
#     return render_template('admin/transaksi/cetakpdf.html', detail=detail, transaksi=transaksi)
#
#     return redirect('adm.transaksi')


if __name__ == '__main__':
    app.run(debug=True)
