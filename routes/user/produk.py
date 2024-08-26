from flask import Blueprint, Flask, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from models.kategori import KategoriModel
from models.produk import ProdukModel

produk = Blueprint("produk", __name__, template_folder="templates", static_folder="static"
                   )

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'


@produk.route('/customer/produk')
@login_required
def productpembeli():
    active_page = 'productpembeli'
    if current_user.role.role_name == 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard_page.dashboard'))
    kategori = KategoriModel.query.all()
    prdk = ProdukModel.query.all()

    return render_template('user/product.html', prdk=prdk, kategori=kategori,
                           active_page=active_page)


@produk.route('/customer/detailprodukpembeli/<id_produk>', methods=['GET', 'POST'])
@login_required
def detailprodukuser(id_produk):
    if current_user.role.role_name == 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard_page.dashboard'))
    produk = ProdukModel.query.filter_by(id_produk=id_produk).first()
    if produk:
        return render_template('user/detailproduk.html', produk=produk)
    return f"Produk dengan id ={id_produk} tidak ada brow "
