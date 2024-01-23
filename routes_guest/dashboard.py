from flask import Blueprint, Flask, redirect, url_for, flash, request, render_template
from flask_login import current_user

from model.kategori import KategoriModel
from model.produk import ProdukModel

landing = Blueprint("landing", __name__, template_folder="templates", static_folder="static"
                 )

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'



# awal page dibuka
@landing.route('/', methods=['POST', 'GET'])
def home():
    active_page = 'home'
    if current_user.is_authenticated:
        if current_user.role == '1':
            return redirect(url_for('dashboard_page.dashboard'))
        else:
            flash("Anda sudah login. Anda tidak diperbolehkan mengakses halaman ini.", "warning")
            return redirect(url_for('dashboard.dashboarduser'))
    kategori = KategoriModel.query.all()
    pilihkategori = request.form.get('id_kategori', 'semua')
    if pilihkategori == 'semua':
        produk_ditemukan = ProdukModel.query.all()
    else:
        produk_ditemukan = ProdukModel.query.filter_by(id_kategori=pilihkategori).all()

    return render_template('guest/index.html', pilihkategori=pilihkategori, prdk=produk_ditemukan,
                           kategori=kategori, active_page=active_page)
