import os

from flask import Blueprint, Flask, flash, url_for, redirect, render_template, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from models.transaksi import TransaksiModel
from models.transaksidetail import TransaksiDetailModel

transaksi = Blueprint("transaksi", __name__, template_folder="templates", static_folder="static"
                      )
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@transaksi.route('/customer/riwayat_pembelian/<id>')
@login_required
def riwayatbeli(id):
    if current_user.role.role_name == 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard_page.dashboard'))
    riwayatpembelian = TransaksiModel.query.filter_by(user_id=id).all()
    return render_template('user/riwayatpembelian.html', riwayatpembelian=riwayatpembelian)



@transaksi.route('/customer/detail_pembelian/<id_transaksi>', methods=['POST', 'GET'])
@login_required
def pembeliandetail(id_transaksi):
    if current_user.role.role_name == 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard_page.dashboard'))
    transaksi = TransaksiModel.query.filter_by(id_transaksi=id_transaksi).first()
    detail = TransaksiDetailModel.query.filter_by(id_transaksi=id_transaksi).all()
    if detail:
        return render_template('user/detailpembelian.html', detail=detail, transaksi=transaksi)
    return f"Produk dengan id ={id_transaksi} tidak ada brow "


@transaksi.route('/customer/riwayat_pembelian/upload_bukti/<id_transaksi>', methods=["GET", "POST"])
@login_required
def upload_bukti(id_transaksi):
    if current_user.role.role_name == 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard_page.dashboard'))
    file = request.files['picture']

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('dashboard_page.dashboard'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        # Update transaction with the picture
        transaksi = TransaksiModel.query.get(id_transaksi)
        if transaksi:
            transaksi.picture = filename
            transaksi.status_pembayaran = '2'  # Set status to 2 as picture is provided
            db.session.commit()

        else:
            flash('Transaction not found', 'danger')
    else:
        flash('Invalid file type', 'danger')

    return redirect(url_for('transaksi.riwayatbeli', id=current_user.id))
