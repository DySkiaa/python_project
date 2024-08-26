from flask import Flask, Blueprint, redirect, url_for, flash, request, render_template, session
from flask_login import current_user, login_user, logout_user

from app import bcrypt, db
from models.produk import ProdukModel
from models.user import Users

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

g_auth = Blueprint(
    "g_auth", __name__, template_folder="templates", static_folder="static"
)


# halaman register
@g_auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.role == '1':
            return redirect(url_for('dashboard_page.dashboard'))
        else:
            flash("Anda sudah login. Anda tidak diperbolehkan mengakses halaman ini.", "warning")
            return redirect(url_for('dashboard.dashboarduser'))
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
            return redirect(url_for('g_auth.register'))

        if len(password) < 5:
            flash('Password harus lebih dari 5 karakter.', 'danger')
            return redirect(url_for('g_auth.register'))

        if len(usia) > 2:
            flash('Usia anda tidak valid.', 'danger')
            return redirect(url_for('g_auth.register'))

        # Cek apakah username sudah ada dalam basis data
        existing_user = Users.query.filter_by(username=username).first()

        if existing_user:
            flash('Username ini sudah digunakan. Silakan pilih username lain.', 'danger')
            return redirect(url_for('g_auth.register'))
        password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')

        user = Users(email=email, username=username, password=password_hashed, fullname=fullname, usia=usia,
                     alamat=alamat, role_id=role_id, notelp=notelp, id_status=id_status)

        db.session.add(user)
        db.session.commit()

        flash('Akun berhasil dibuat. Anda dapat login sekarang.', 'success')
        return redirect(url_for('g_auth.login'))
    return render_template('guest/register.html')


# login semua role(logika user admin ada di dalam fungsi)
@g_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == '1':
            return redirect(url_for('dashboard_page.dashboard'))
        else:
            flash("Anda sudah login. Anda tidak diperbolehkan mengakses halaman ini.", "warning")
            return redirect(url_for('dashboard.dashboarduser'))
    if request.method == 'POST':
        username_atau_email = request.form['username_atau_email']
        password = request.form['password']

        user = Users.query.filter(
            (Users.username == username_atau_email) | (Users.email == username_atau_email)).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login berhasil!', 'success')
            if user.role.role_name == 'admin':
                return redirect(url_for('dashboard_page.dashboard'))
            else:
                return redirect(url_for('dashboard.dashboarduser'))
        else:
            flash('Login gagal. Periksa kembali username dan kata sandi Anda.', 'danger')

    return render_template('guest/login.html')


@g_auth.route('/logout')
def logout():
    if 'cart' in session:
        cart_items = session['cart']
        for cart in cart_items:
            id_produk = cart['id_produk']
            quantity = cart['quantity']
            product = ProdukModel.query.get(id_produk)
            if product:
                product.stok += quantity
                db.session.commit()
        del session['cart']
    logout_user()
    flash('Berhasil Logout!', 'success')
    return redirect(url_for("landing.home"))
