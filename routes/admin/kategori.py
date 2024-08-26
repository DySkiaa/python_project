from flask import Blueprint, flash, url_for, redirect, render_template, request, Flask
from flask_login import login_required, current_user

from app import db
from models.kategori import KategoriModel

kategori_page = Blueprint("kategori_page", __name__, template_folder="templates", static_folder="static")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

@kategori_page.route('/admin/kategori')
@login_required
def kategori():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Dashboard', 'Kategori']  # Data breadcrumb
    ktgr = KategoriModel.query.all()
    return render_template('admin/kategori/index.html', ktgr=ktgr, breadcrumb_data=breadcrumb_data)


# halaman tambah kategori
@kategori_page.route('/admin/kategori/tambahkategori', methods=['GET', 'POST'])
@login_required
def tambahkategori():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Kategori', 'Tambah kategori']  # Data breadcrumb
    if request.method == 'GET':
        return render_template('admin/kategori/tambahkategori.html', breadcrumb_data=breadcrumb_data)
    if request.method == 'POST':
        kategori = request.form['kategori']
        kategori = KategoriModel(kategori=kategori)
        db.session.add(kategori)
        db.session.commit()
        flash('Kategori Berhasil Di Tambahkan!', 'success')
        return redirect(url_for('.kategori'))
    return render_template('admin/kategori/tambahkategori.html', breadcrumb_data=breadcrumb_data)


# halaman edit kategori
@kategori_page.route('/admin/kategori/editktgr/<id_kategori>', methods=['GET', 'POST'])
@login_required
def editktgr(id_kategori):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    kategori = KategoriModel.query.get(id_kategori)
    breadcrumb_data = ['Kategori', 'Edit kategori']  # Data breadcrumb
    if request.method == 'POST':
        if kategori:
            # Update data kategori dengan data baru dari formulir
            kategori.kategori = request.form['kategori']

            db.session.commit()
            flash('Kategori Berhasil Di Edit!', 'success')
            return redirect(url_for('.kategori'))
        return f"Kategori dengan ID = {id_kategori} tersebut tidak ada"

    return render_template('admin/kategori/editktgr.html', kategori=kategori, breadcrumb_data=breadcrumb_data)


# halaman delet kategori
@kategori_page.route("/admin/kategori/deletektgr/<id_kategori>", methods=["GET", "POST"])
@login_required
def deletektgr(id_kategori):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    kategori = KategoriModel.query.filter_by(id_kategori=id_kategori).first()
    breadcrumb_data = ['Kategori', 'Hapus Kategori']  # Data breadcrumb
    if request.method == 'POST':
        if kategori:
            db.session.delete(kategori)
            db.session.commit()
            flash('Kategori  Berhasil Di Hapus!', 'success')
            return redirect(url_for('adm.kategori'))

    return render_template('deletepages.html', kategori=kategori, breadcrumb_data=breadcrumb_data)

