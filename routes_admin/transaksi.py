from flask import Flask, Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from model.transaksi import TransaksiModel
from model.transaksidetail import TransaksiDetailModel

transaksi_page = Blueprint("transaksi_page", __name__, template_folder="templates", static_folder="static"
                )
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

@transaksi_page.route('/admin/transaksi')
@login_required
def transaksi():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Dashboard', 'Transaksi']  # Data breadcrumb
    transaksi = TransaksiModel.query.all()
    return render_template('admin/transaksi/index.html', transaksi=transaksi, breadcrumb_data=breadcrumb_data)


# halaman detail transaksi
@transaksi_page.route('/admin/transaksi/detailtransaksi/<id_transaksi>', methods=['POST', 'GET'])
@login_required
def transaksidetail(id_transaksi):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))

    breadcrumb_data = ['Transaksi', 'Detail Transaksi']  # Data breadcrumb
    transaksi = TransaksiModel.query.filter_by(id_transaksi=id_transaksi).first()
    detail = TransaksiDetailModel.query.filter_by(id_transaksi=id_transaksi).all()
    if detail:
        return render_template('admin/transaksi/detailtransaksi.html', detail=detail, transaksi=transaksi,
                               breadcrumb_data=breadcrumb_data)
    return f"Produk dengan id ={id_transaksi} tidak ada brow "


@transaksi_page.route('/admin/transaksi/cetakpdf/<id_transaksi>')
@login_required
def cetakpdf(id_transaksi):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    transaksi = TransaksiModel.query.filter_by(id_transaksi=id_transaksi).first()
    detail = TransaksiDetailModel.query.filter_by(id_transaksi=id_transaksi).all()
    return render_template('admin/transaksi/cetakpdf.html', detail=detail, transaksi=transaksi)

    return redirect('.transaksi')