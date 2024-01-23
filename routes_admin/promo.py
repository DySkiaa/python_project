from flask import Blueprint, flash, redirect, url_for, render_template, request, Flask
from flask_login import login_required, current_user

from app import db
from model.produk import ProdukModel
from model.promo import PromoModel

promo_page = Blueprint("promo_page", __name__, template_folder="templates", static_folder="static")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

@promo_page.route('/admin/promo')
@login_required
def promo():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Dashboard', 'Promo']  # Data breadcrumb
    promo = PromoModel.query.all()

    return render_template('admin/promo/index.html', breadcrumb_data=breadcrumb_data, promo=promo)


@promo_page.route('/admin/promo/buatpromo', methods=['POST', 'GET'])
@login_required
def buatpromo():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Promo', 'Buat Promo']  # Data breadcrumb
    if request.method == 'GET':
        return render_template('admin/promo/buatpromo.html', breadcrumb_data=breadcrumb_data)
    if request.method == 'POST':
        nama_promo = request.form['nama_promo']
        diskon = request.form['diskon']
        promo = PromoModel(nama_promo=nama_promo, diskon=diskon)
        db.session.add(promo)
        db.session.commit()
        flash('Kategori Berhasil Di Tambahkan!', 'success')
        return redirect(url_for('.promo'))

    return render_template('admin/promo/buatpromo.html', breadcrumb_data=breadcrumb_data)

@promo_page.route('/admin/promo/editpromo/<id_promo>', methods=['GET', 'POST'])
@login_required
def editpromo(id_promo):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    promo = PromoModel.query.get(id_promo)
    breadcrumb_data = ['Promo', 'Edit Promo']  # Data breadcrumb
    if request.method == 'POST':
        if promo:
            # Update data kategori dengan data baru dari formulir
            promo.nama_promo = request.form['nama_promo']
            promo.diskon = request.form['diskon']

            db.session.commit()
            flash('Promo Berhasil Di Edit!', 'success')
            return redirect(url_for('.promo'))
        return f"Kategori dengan ID = {id_promo} tersebut tidak ada"

    return render_template('admin/promo/editpromo.html', promo=promo, breadcrumb_data=breadcrumb_data)

@promo_page.route('/admin/promo/deletepromo/<id_promo>', methods=['POST', 'GET'])
@login_required
def deletepromo(id_promo):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    promo = PromoModel.query.filter_by(id_promo=id_promo).first()
    breadcrumb_data = ['Promo', 'Hapus Promo']  # Data breadcrumb
    if request.method == 'POST':
        if promo:
            db.session.delete(promo)
            db.session.commit()
            flash('Promo  Berhasil Di Hapus!', 'success')
            return redirect(url_for('.promo'))

    return render_template('deletepages.html', promo=promo, breadcrumb_data=breadcrumb_data)


