from datetime import datetime
from sqlite3 import IntegrityError


from flask import Blueprint, flash, redirect, url_for, render_template, request, session, Flask
from flask_login import login_required, current_user

from app import db, bcrypt
from model.kategori import KategoriModel
from model.produk import ProdukModel
from model.promo import PromoModel
from model.transaksi import TransaksiModel
from model.transaksidetail import TransaksiDetailModel
from model.user import Users
# from models import Transaksi, DetailTransaksi, Users, category, Product, bcrypt, Promo
# from routes_admin.landing import user

dashboard = Blueprint("dashboard", __name__, template_folder="templates", static_folder="static"
                 )

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'


# buat table
@dashboard.before_app_request
def create_tables():
    db.create_all()


# untuk current time
@dashboard.context_processor
def inject_current_datetime():
    return dict(current_datetime=datetime.now())


@dashboard.route('/customer/dashboard', methods=['POST', 'GET'])
@login_required
def dashboarduser():
    if current_user.role.role_name == 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard_page.dashboard'))

    active_page = 'dashboarduser'
    kategori = KategoriModel.query.all()
    pilihkategori = request.form.get('id_kategori', 'semua')
    if pilihkategori == 'semua':
        produk_ditemukan = ProdukModel.query.limit(4).all()
    else:
        produk_ditemukan = ProdukModel.query.filter_by(id_kategori=pilihkategori).limit(4).all()

    return render_template('user/dashboard.html', pilihkategori=pilihkategori, prdk=produk_ditemukan,
                           kategori=kategori, active_page=active_page)


# ganti password user
@dashboard.route('/customer/change_password', methods=['GET', 'POST'])
@login_required
def gantipassworduser():
    if current_user.role.role_name == 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard_page.dashboard'))

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if bcrypt.check_password_hash(current_user.password, old_password):
            if new_password == confirm_password:
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                current_user.password = hashed_password
                db.session.commit()
                flash('Kata sandi telah diganti.', 'success')
                return redirect(url_for('cust.dashboarduser'))
            elif new_password == old_password:
                flash('Kata sandi baru harus berbeda dari kata sandi lama.', 'warning')
            else:
                flash('Konfirmasi kata sandi tidak cocok.', 'warning')
        else:
            flash('Kata sandi lama salah.', 'warning')

    return render_template('user/changepassword.html')


# halaman detail akun user
@dashboard.route('/customer/detailaccountuser/<id>', methods=['GET', 'POST'])
@login_required
def detailaccountuser(id):
    if current_user.role.role_name == 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard_page.home'))
    user = Users.query.get(id)
    if user and user == current_user:
        new_fullname = None
        new_usia = None
        new_alamat = None
        new_notelp = None
        if request.method == 'POST':
            new_fullname = request.form.get('new_fullname')
            new_usia = request.form.get('new_usia')
            new_alamat = request.form.get('new_alamat')
            new_notelp = request.form.get('new_notelp')

            user.fullname = new_fullname
            user.usia = new_usia
            user.alamat = new_alamat
            user.notelp = new_notelp
            db.session.commit()
            flash('Profil berhasil diperbarui.', 'success')
            return redirect(url_for('cust.dashboarduser', id=id))

        return render_template('user/detailuser.html', user=user, new_usia=new_usia, new_alamat=new_alamat,
                               new_fullname=new_fullname, new_notelp=new_notelp)

