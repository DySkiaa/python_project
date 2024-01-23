
from flask import Blueprint, Flask, flash, redirect, url_for, render_template, request
from flask_login import current_user, login_required

from app import db
from model.kategori import KategoriModel
from model.produk import ProdukModel

produk_page = Blueprint("produk_page", __name__, template_folder="templates", static_folder="static"
                )
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

@produk_page.route('/admin/produk')
@login_required
def product():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Dashboard', 'Produk']  # Data breadcrumb
    prdk = ProdukModel.query.all()
    return render_template('admin/produk/index.html', prdk=prdk, breadcrumb_data=breadcrumb_data)


# halaman tambah produk (hanya admin)
@produk_page.route('/admin/produk/tambahproduk', methods=['GET', 'POST'])
@login_required
def tambahproduk():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))

    kategori = KategoriModel.query.all()
    breadcrumb_data = ['Produk', 'Tambah Produk']  # Data breadcrumb
    if request.method == 'GET':
        return render_template('admin/produk/tambahproduk.html', breadcrumb_data=breadcrumb_data, kategori=kategori)
    if request.method == 'POST':
        nama_product = request.form['nama_product']
        deskripsi = request.form['deskripsi']
        id_kategori = request.form['id_kategori']
        harga = float(request.form['harga'])
        gambar = request.form['gambar']
        stok = int(request.form['stok'])
        id_promo = None
        status = 1
        selling = 0

        if harga < 0 or stok < 0:
            flash('Harga dan stok tidak boleh kurang dari 0.', 'warning')
            return redirect(url_for('.tambahproduk'))

        produk = ProdukModel(nama_product=nama_product, deskripsi=deskripsi, id_kategori=id_kategori, harga=harga,
                         gambar=gambar, stok=stok, id_promo=id_promo, id_status=status, selling=selling)

        db.session.add(produk)
        db.session.commit()
        flash('Data Produk Berhasil Di Input!', 'success')
        return redirect(url_for('.product'))

    return render_template('admin/produk/tambahproduk.html', breadcrumb_data=breadcrumb_data)


# halaman edit produk(hanya admin)
@produk_page.route('/admin/produk/editproduk/<id_produk>', methods=['GET', 'POST'])
@login_required
def editproduk(id_produk):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Produk', 'Edit Produk']  # Data breadcrumb
    produk = ProdukModel.query.filter_by(id_produk=id_produk).first()
    kategori_option = KategoriModel.query.all()

    if request.method == 'POST':

        nama_product = request.form['nama_product']
        deskripsi = request.form['deskripsi']
        id_kategori = request.form['id_kategori']
        harga = float(request.form['harga'])
        gambar = request.form['gambar']

        if harga < 0:
            flash('Harga tidak boleh kurang dari 0.', 'warning')
            return redirect(url_for('adm.editproduk', id_produk=id_produk))
        # Cek apakah kolom gambar diisi atau tidak
        if not gambar:
            # Jika tidak diisi, gunakan gambar saat ini
            gambar = produk.gambar

        produk.nama_product = nama_product
        produk.deskripsi = deskripsi
        produk.id_kategori = id_kategori
        produk.harga = harga
        produk.gambar = gambar

        db.session.commit()
        flash('Produk Berhasil Di Edit!', 'success')
        return redirect(url_for('.product'))

        return f"Produk dengan ID = {id_produk} tersebut tidak ada"

    return render_template('admin/produk/editproduk.html', breadcrumb_data=breadcrumb_data, produk=produk,
                           kategori_option=kategori_option)


# tambah stok produk
@produk_page.route('/admin/produk/tambahstok/<id_produk>', methods=['GET', 'POST'])
@login_required
def tambahstok(id_produk):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))

    breadcrumb_data = ['Produk', 'Tambah Stok']  # Data breadcrumb

    produk = ProdukModel.query.get(id_produk)

    if not produk:
        return "Produk dengan ID tersebut tidak ditemukan"

    if request.method == 'POST':
        stok_tambahan = int(request.form['stok'])

        if stok_tambahan < 0:
            flash('Jumlah stok yang diinput tidak valid.', 'warning')
        else:
            stok_baru = stok_tambahan
            produk.stok = stok_baru
            db.session.commit()
            flash('Stok Produk Berhasil Ditambah!', 'success')
            return redirect(url_for('.product'))

    return render_template('admin/produk/tambahstok.html', produk=produk, breadcrumb_data=breadcrumb_data)


# halaman detail (produk)
@produk_page.route('/admin/produk/detailproduk/<id_produk>')
@login_required
def detailproduk(id_produk):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    produk = ProdukModel.query.filter_by(id_produk=id_produk).first()
    breadcrumb_data = ['Produk', 'Detail Produk']  # Data breadcrumb
    if produk:
        return render_template('admin/produk/detailproduk.html', produk=produk, breadcrumb_data=breadcrumb_data)
    return f"Produk dengan id ={id_produk} tidak ada brow "


@produk_page.route('/admin/produk/aktifkan/<id_produk>', methods=['GET', 'POST'])
@login_required
def aktifkan(id_produk):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    produk = ProdukModel.query.get(id_produk)
    if produk:
        produk.id_status = 1
        try:
            db.session.commit()
            flash('Produk berhasil diaktifkan.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat menyimpan perubahan.', 'danger')
            print(e)
        finally:
            db.session.close()

        return redirect(
            url_for('.product'))  # Gantilah 'halaman_karyawan' dengan nama rute halaman karyawan Anda
    else:
        flash('produk tidak ditemukan.', 'danger')
        return redirect(url_for('.product'))

@produk_page.route('/admin/produk/nonaktif/<id_produk>', methods=['GET', 'POST'])
@login_required
def nonaktifproduk(id_produk):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    produk = ProdukModel.query.get(id_produk)
    if produk:
        produk.id_status = 2
        try:
            db.session.commit()
            flash('Produk berhasil dinonaktifkan.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat menyimpan perubahan.', 'danger')
            print(e)
        finally:
            db.session.close()

        return redirect(
            url_for('.product'))  # Gantilah 'halaman_karyawan' dengan nama rute halaman karyawan Anda
    else:
        flash('produk tidak ditemukan.', 'danger')
        return redirect(url_for('.product'))


