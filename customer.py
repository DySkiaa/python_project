# from datetime import datetime
# from sqlite3 import IntegrityError
#
# from flask import Blueprint, flash, redirect, url_for, render_template, request, session, Flask
# from flask_login import login_required, current_user
#
# from app import db
# from models import Transaksi, DetailTransaksi, Users, category, Product, bcrypt, Promo
# from routes_admin.landing import user
#
# cust = Blueprint("cust", __name__, template_folder="templates", static_folder="static"
#                  )
#
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static/images'
#
#
# # buat table
# @cust.before_app_request
# def create_tables():
#     db.create_all()
#
#
# # untuk current time
# @cust.context_processor
# def inject_current_datetime():
#     return dict(current_datetime=datetime.now())
#
#
# @cust.routes_admin('/dashboard', methods=['POST', 'GET'])
# @login_required
# def dashboarduser():
#     if current_user.role.role_name == 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('adm.dashboard'))
#
#     active_page = 'dashboarduser'
#     kategori = category.query.all()
#     pilihkategori = request.form.get('id_kategori', 'semua')
#     if pilihkategori == 'semua':
#         produk_ditemukan = Product.query.limit(4).all()
#     else:
#         produk_ditemukan = Product.query.filter_by(id_kategori=pilihkategori).limit(4).all()
#
#     return render_template('user/dashboard.html', pilihkategori=pilihkategori, prdk=produk_ditemukan,
#                            kategori=kategori, active_page=active_page)
#
#
# # ganti password user
# @cust.routes_admin('/change_password_user', methods=['GET', 'POST'])
# @login_required
# def gantipassworduser():
#     if current_user.role.role_name == 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('adm.dashboard'))
#
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
#                 return redirect(url_for('cust.dashboarduser'))
#             elif new_password == old_password:
#                 flash('Kata sandi baru harus berbeda dari kata sandi lama.', 'warning')
#             else:
#                 flash('Konfirmasi kata sandi tidak cocok.', 'warning')
#         else:
#             flash('Kata sandi lama salah.', 'warning')
#
#     return render_template('user/changepassword.html')
#
#
# # halaman detail akun user
# @cust.routes_admin('/detailaccountuser/<int:id>', methods=['GET', 'POST'])
# @login_required
# def detailaccountuser(id):
#     if current_user.role.role_name == 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('adm.home'))
#     user = Users.query.get(id)
#     if user and user == current_user:
#         new_fullname = None
#         new_usia = None
#         new_alamat = None
#         new_notelp = None
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
#             return redirect(url_for('cust.dashboarduser', id=id))
#
#         return render_template('user/detailadmin.html', user=user, new_usia=new_usia, new_alamat=new_alamat,
#                                new_fullname=new_fullname, new_notelp=new_notelp)
#
#
# # halaman product (setelah login)
# @cust.routes_admin('/produk')
# @login_required
# def productpembeli():
#     active_page = 'productpembeli'
#     if current_user.role.role_name == 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('adm.dashboard'))
#     kategori = category.query.all()
#     prdk = Product.query.all()
#
#     return render_template('user/product.html', prdk=prdk, kategori=kategori,
#                            active_page=active_page)
#
#
# # halaman cari produk berdasarkan kategori produk (setelah login)
# @cust.routes_admin('/produk', methods=['POST'])
# @login_required
# def cari_produk_user():
#     active_page = 'productpembeli'
#     if current_user.role.role_name == 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('adm.dashboard'))
#     kategori = category.query.all()
#
#     if request.method == 'POST':
#         kategori_terpilih = request.form.get('id_kategori', 'semua')
#
#         if kategori_terpilih == 'semua':
#             produk_ditemukan = Product.query.all()
#         else:
#             produk_ditemukan = Product.query.filter_by(id_kategori=kategori_terpilih).all()
#     else:
#         # Jika bukan metode POST, tampilkan semua produk
#         produk_ditemukan = Product.query.all()
#
#     return render_template('user/product.html', active_page=active_page,
#                            kategori_terpilih=kategori_terpilih, prdk=produk_ditemukan, kategori=kategori)
#
#
# @cust.routes_admin('/detailprodukpembeli/<int:id_produk>', methods=['GET', 'POST'])
# @login_required
# def detailprodukuser(id_produk):
#     if current_user.role.role_name == 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('adm.dashboard'))
#     produk = Product.query.filter_by(id_produk=id_produk).first()
#     if produk:
#         return render_template('user/detailproduk.html', produk=produk)
#     return f"Produk dengan id ={id_produk} tidak ada brow "
#
#
# def init_shopping_cart():
#     if 'cart' not in session:
#         session['cart'] = []
#
#
# @cust.routes_admin('/add_to_cart/<int:id_produk>', methods=['POST'])
# @login_required
# def add_to_cart(id_produk):
#     init_shopping_cart()
#
#     produk = Product.query.get(id_produk)
#     if produk:
#         quantity = int(request.form.get('quantity'))
#         available_stock = produk.stok  # Get the available stock for the product
#
#         if quantity <= 0:
#             flash('Jumlah produk harus lebih dari 0', 'danger')
#             return redirect(url_for('cust.productpembeli'))
#         if quantity <= available_stock:
#
#             # Mengecek jika produk sudah ada di keranjang
#             for item in session['cart']:
#
#                 if item['id_produk'] == produk.id_produk:
#
#                     # Jika barang yang sama dimasukkan maka akan menambahkan quantity
#                     if item['quantity'] + quantity <= available_stock:
#
#                         promo = Promo.query.get(produk.id_promo)
#                         item['quantity'] += quantity
#                         if promo:
#                             diskon_harga = produk.harga - (produk.harga * (promo.diskon / 100))
#                             item['diskon_harga'] = diskon_harga
#                             item['subtotal'] = diskon_harga * item['quantity']
#                         else:
#                             item['subtotal'] = item['harga'] * item['quantity']
#                         flash('Produk quantity telah diperbarui', 'success')
#
#                         # Kurangi stok yang tersedia
#                         produk.stok -= quantity
#                         db.session.commit()
#                     else:
#                         flash('Jumlah yang diminta melebihi stok yang tersedia', 'error')
#                     break
#             else:
#                 # Jika tidak ada di keranjang maka akan dimasukkan menjadi barang baru yang dimasukkan ke keranjang
#                 promo = Promo.query.get(produk.id_promo)
#
#                 if produk.id_promo is not None:
#                     diskon_harga = produk.harga - (produk.harga * (promo.diskon / 100))
#                     if promo:
#                         subtotal = diskon_harga * quantity
#                     else:
#                         subtotal = produk.harga * quantity
#                 else:
#                     subtotal = produk.harga * quantity
#
#                 # Cek apakah produk sudah ada di keranjang
#                 product_in_cart = False
#                 for item in session['cart']:
#                     if item['id_produk'] == produk.id_produk:
#                         product_in_cart = True
#                         break
#
#                 if not product_in_cart:
#                     item = {
#                         'id_produk': produk.id_produk,
#                         'harga': produk.harga,
#                         'nama_product': produk.nama_product,
#                         'gambar': produk.gambar,
#                         'diskon': promo.diskon if promo else None,
#                         'quantity': quantity,
#                         'diskon_harga': diskon_harga if promo else 0,
#                         'subtotal': subtotal
#                     }
#                     session['cart'].append(item)
#                     # Kurangi stok yang tersedia
#                     produk.stok -= quantity
#                     db.session.commit()
#                     flash('Produk sudah ditambahkan ke keranjang', 'success')
#         else:
#             flash('Stok produk tidak mencukupi', 'danger')
#         return redirect(url_for('cust.productpembeli'))
#     else:
#         flash('Produk tidak ada', 'danger')
#
#     return redirect(url_for('cust.cart'))
#
# @cust.routes_admin('/cart')
# @login_required
# def cart():
#     if current_user.role.role_name == 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('adm.dashboard'))
#     active_page = 'cart'
#     init_shopping_cart()
#     cart = session['cart']
#     # Jika keranjang masih kosong
#     if not cart:
#         flash('Keranjang Anda kosong. Silakan tambahkan produk terlebih dahulu.', 'info')
#         return redirect(url_for('cust.productpembeli'))
#     total = sum(item['subtotal'] for item in session['cart'])
#
#     return render_template('user/cart.html', cart=cart, total=total, active_page=active_page)
#
# @cust.routes_admin('/remove_from_cart/<int:id_produk>', methods=['POST'])
# @login_required
# def remove_from_cart(id_produk):
#     if 'cart' in session:
#         for item in session['cart']:
#             if item['id_produk'] == id_produk:
#                 product = Product.query.get(id_produk)
#                 product.stok += item['quantity']
#                 db.session.commit()
#                 session['cart'].remove(item)
#                 return redirect(url_for('cust.cart'))
#
#
# @cust.routes_admin('/checkout', methods=['POST'])
# @login_required
# def checkout():
#     if current_user.role.role_name == 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('adm.dashboard'))
#     init_shopping_cart()
#
#     user_id = current_user.id  # Replace with actual user ID
#     date = datetime.now()
#     total = sum(item['subtotal'] for item in session['cart'])
#
#     transaksi = Transaksi(user_id=user_id, date=date, total=total)
#     db.session.add(transaksi)
#     db.session.commit()
#
#     for item in session['cart']:
#         detail_transaksi = DetailTransaksi(
#             id_transaksi=transaksi.id_transaksi,
#             id_produk=item['id_produk'],
#             quantity=item['quantity'],
#             subtotal=item['subtotal'],
#
#         )
#         db.session.add(detail_transaksi)
#
#     #     # Kurangkan stok produk
#     #     produk = Product.query.get(item['id_produk'])
#     #     produk.stok -= item['quantity']
#     #
#     # db.session.commit()
#
#     try:
#         session.pop('cart')
#         flash('Pembelian berhasil', 'success')
#     except IntegrityError:
#         db.session.rollback()
#         flash('Error dalam pembelian', 'danger')
#
#     return redirect(url_for('cust.dashboarduser'))
#
#
# @cust.routes_admin('/riwayat_pembelian/<int:id>')
# @login_required
# def riwayatbeli(id):
#     if current_user.role.role_name == 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('adm.dashboard'))
#     riwayatpembelian = Transaksi.query.filter_by(user_id=id).all()
#     return render_template('user/riwayatpembelian.html', riwayatpembelian=riwayatpembelian)
#
#
# @cust.routes_admin('/detail_pembelian/<int:id_transaksi>', methods=['POST', 'GET'])
# @login_required
# def pembeliandetail(id_transaksi):
#     if current_user.role.role_name == 'admin':
#         flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
#         return redirect(url_for('admin.dashboard'))
#     transaksi = Transaksi.query.filter_by(id_transaksi=id_transaksi).first()
#     detail = DetailTransaksi.query.filter_by(id_transaksi=id_transaksi).all()
#     if detail:
#         return render_template('user/detailpembelian.html', detail=detail, transaksi=transaksi)
#     return f"Produk dengan id ={id_transaksi} tidak ada brow "
