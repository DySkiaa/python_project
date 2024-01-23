from flask import Blueprint, Flask, redirect, url_for, flash, request, render_template
from flask_login import current_user

from model.kategori import KategoriModel
from model.produk import ProdukModel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

g_prod = Blueprint(
    "g_prod", __name__, template_folder="templates", static_folder="static"
)


# halaman produk (tidak perlu login)
@g_prod.route('/produk')
def productuser():
    active_page = 'productuser'
    if current_user.is_authenticated:
        if current_user.role == '1':
            return redirect(url_for('dashboard_page.dashboard'))
        else:
            flash("Anda sudah login. Anda tidak diperbolehkan mengakses halaman ini.", "warning")
            return redirect(url_for('dashboard.dashboarduser'))
    kategori = KategoriModel.query.all()
    prdk = ProdukModel.query.all()
    return render_template('guest/produkuser.html', prdk=prdk, kategori=kategori, active_page=active_page)


@g_prod.route('/detail_produk/<id_produk>', methods=['GET', 'POST'])
def detailproduknotlogin(id_produk):
    produk = ProdukModel.query.filter_by(id_produk=id_produk).first()
    if produk:
        return render_template('guest/detailproduk.html', produk=produk)
    return f"Produk dengan id ={id_produk} tidak ada brow "
