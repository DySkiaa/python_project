from flask import Flask, Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from app import db, bcrypt
from model.produk import ProdukModel
from model.transaksi import TransaksiModel
from model.user import Users

dashboard_page = Blueprint("dashboard_page", __name__, template_folder="templates", static_folder="static")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'


@dashboard_page.route('/admin/dashboard')
@login_required
def dashboard():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))

    breadcrumb_data = ['Dashboard', 'Home']  # Data breadcrumb
    transaksi = TransaksiModel.query.all()
    produk = ProdukModel.query.all()
    cust = Users.query.filter_by(role_id=2).all()

    cust = len(cust)
    produk = len(produk)
    total = sum(transaksi.total for transaksi in transaksi)
    transaksi = len(transaksi)
    return render_template('admin/dashboard.html', cust=cust, produk=produk, total=total,
                           breadcrumb_data=breadcrumb_data, transaksi=transaksi)


# halaman detail akun admin
@dashboard_page.route('/admin/dashboard/detailakun/<id>', methods=['GET', 'POST'])
@login_required
def detailakun(id):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    user = Users.query.get(id)
    breadcrumb_data = ['Dashboard', 'Detail Akun']  # Data breadcrumb
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
            return redirect(url_for('dashboard_page.dashboard', id=id))

        return render_template('admin/detailadmin.html', user=user, new_usia=new_usia, new_alamat=new_alamat,
                               new_fullname=new_fullname, new_notelp=new_notelp, breadcrumb_data=breadcrumb_data)


# register akun admin
@dashboard_page.route('/admin/dashboard/addadmin', methods=['GET', 'POST'])
@login_required
def addadmin():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Dashboard', 'Tambah Akun Admin']  # Data breadcrumb
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        usia = request.form['usia']
        alamat = request.form['alamat']
        role_id = request.form['role_id']
        notelp = request.form['notelp']
        id_status = 1

        if len(username) < 5:
            flash('Username harus lebih dari 5 karakter.', 'danger')
            return redirect(url_for('adm.addadmin'))

        if len(password) < 5:
            flash('Password harus lebih dari 5 karakter.', 'danger')
            return redirect(url_for('adm.addadmin'))

        if len(usia) > 2:
            flash('Usia anda sepertinya tidak masuk akal.', 'danger')
            return redirect(url_for('adm.addadmin'))

        # Cek apakah username sudah ada dalam basis data
        existing_user = Users.query.filter_by(username=username).first()

        if existing_user:
            flash('Username ini sudah digunakan. Silakan pilih username lain.', 'danger')
            return redirect(url_for('adm.addadmin'))
        password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')

        user = Users(email=email, username=username, password=password_hashed, fullname=fullname, usia=usia,
                     alamat=alamat,
                     role_id=role_id, notelp=notelp, id_status=id_status)

        db.session.add(user)
        db.session.commit()

        flash('Akun berhasil dibuat.', 'success')
        return redirect(url_for('dashboard_page.dashboard'))
    return render_template('admin/addadmin.html', breadcrumb_data=breadcrumb_data)


# ganti password admin
@dashboard_page.route('/admin/dashboard/change_password', methods=['GET', 'POST'])
@login_required
def gantipassword():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))

    breadcrumb_data = ['Dashboard', 'Ganti Password']  # Data breadcrumb
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
                return redirect(url_for('dashboard_page.dashboard'))
            elif new_password == old_password:
                flash('Kata sandi baru harus berbeda dari kata sandi lama.', 'warning')
            else:
                flash('Konfirmasi kata sandi tidak cocok.', 'warning')
        else:
            flash('Kata sandi lama salah.', 'warning')

    return render_template('admin/change_password.html', breadcrumb_data=breadcrumb_data)
