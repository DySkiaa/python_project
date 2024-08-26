import os

from docx import Document
from flask import Flask, Blueprint, flash, redirect, url_for, render_template, send_file, current_app, request
from flask_login import login_required, current_user

from app import db
from models.transaksi import TransaksiModel
from models.transaksidetail import TransaksiDetailModel

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


@transaksi_page.route('/admin/transaksi/cekbukti/<id_transaksi>')
@login_required
def cekbukti(id_transaksi):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Transaksi', 'Cek Bukti']
    transaksi = TransaksiModel.query.filter_by(id_transaksi=id_transaksi).first()
    detail = TransaksiDetailModel.query.filter_by(id_transaksi=id_transaksi).all()
    return render_template('admin/transaksi/cekbukti.html', detail=detail, transaksi=transaksi,
                           breadcrumb_data=breadcrumb_data)


@transaksi_page.route('/admin/transaksi/cekbukti/terima/<id_transaksi>')
@login_required
def terima_cek_bukti(id_transaksi):
    transaksi = TransaksiModel.query.get(id_transaksi)
    if transaksi:
        transaksi.status_pembayaran = 3
        db.session.commit()
    else:
        flash('Transaksi tidak ditemukan.', 'danger')
    return redirect(url_for('transaksi_page.transaksi'))


@transaksi_page.route('/admin/transaksi/update_status/<id_transaksi>', methods=['POST'])
@login_required
def update_status(id_transaksi):
    status = request.form.get('status')
    transaksi = TransaksiModel.query.get(id_transaksi)
    if transaksi:
        if status == "3":
            transaksi.status_pembayaran = 3
        elif status == "4":
            transaksi.status_pembayaran = 4
        db.session.commit()
    else:
        flash('Transaksi tidak ditemukan.', 'danger')
    return redirect(url_for('transaksi_page.transaksi'))
