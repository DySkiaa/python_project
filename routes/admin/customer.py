from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from models.transaksi import TransaksiModel
from models.user import Users

customer_page = Blueprint("customer_page", __name__, template_folder="templates", static_folder="static")


@customer_page.route('/admin/customer')
@login_required
def customer():
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Dashboard', 'Customer']  # Data breadcrumb
    user = Users.query.filter_by(role_id='2').all()
    return render_template('admin/customer/index.html', user=user, breadcrumb_data=breadcrumb_data)


# halaman transaksi yang dicari sesuai dari user_id
@customer_page.route('/admin/customer/riwayat_transaksi/<user_id>')
@login_required
def riwayat(user_id):
    if current_user.role.role_name != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard.dashboarduser'))
    breadcrumb_data = ['Customer', 'Transaksi']  # Data breadcrumb
    riwayattransaksi = TransaksiModel.query.filter_by(user_id=user_id).all()
    transaksi = TransaksiModel.query.filter_by(user_id=user_id).first()
    user = Users.query.filter_by(id=user_id).first()
    return render_template('admin/transaksi/riwayat.html', user=user, breadcrumb_data=breadcrumb_data, riwayattransaksi=riwayattransaksi, transaksi=transaksi)

