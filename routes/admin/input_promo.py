from flask import Blueprint, flash, redirect, url_for, render_template, request, Flask
from flask_login import login_required, current_user

from app import db
from models.produk import ProdukModel
from models.promo import PromoModel

input_promo_page = Blueprint("input_promo_page", __name__, template_folder="templates", static_folder="static")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'


@input_promo_page.route('/admin/input_promo')
@login_required
def tambahpromo():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Promo', 'Tambah Promo']  # Data breadcrumb
    prdk = ProdukModel.query.all()
    # promo = Promo.query.all()

    return render_template('admin/input_promo/index.html', produk=prdk, breadcrumb_data=breadcrumb_data)


@input_promo_page.route('/admin/input_promo/tambahpromoproduk/<id_produk>', methods=['POST', 'GET'])
@login_required
def tambahpromoproduk(id_produk):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Promo', 'Tambah Promo Produk']  # Data breadcrumb
    promo = PromoModel.query.all()
    produk = ProdukModel.query.get(id_produk)

    if request.method == 'GET':
        return render_template('admin/input_promo/tambahpromo.html', promo=promo, breadcrumb_data=breadcrumb_data, )
    if request.method == 'POST':
        id_promo = int(request.form['id_promo'])
        produk.id_promo = id_promo
        db.session.commit()

        flash('Promo Produk Berhasil Ditambah!', 'success')
        return redirect(url_for('.tambahpromo'))


@input_promo_page.route('/admin/input_promo/<id_produk>', methods=['POST', 'GET'])
@login_required
def cabutpromo(id_produk):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    produk = ProdukModel.query.get(id_produk)

    if produk:
        produk.id_promo = None
        db.session.commit()
        flash('Promo telah dicabut dari produk.', 'success')
    else:
        flash('Produk tidak ditemukan.', 'warning')

    return redirect(url_for('.tambahpromo'))
