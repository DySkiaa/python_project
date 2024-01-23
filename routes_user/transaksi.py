from flask import Blueprint, Flask, flash, url_for, redirect, render_template
from flask_login import login_required, current_user

from model.transaksi import TransaksiModel
from model.transaksidetail import TransaksiDetailModel

transaksi = Blueprint("transaksi", __name__, template_folder="templates", static_folder="static"
                 )
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

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
