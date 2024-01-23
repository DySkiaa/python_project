from flask import Blueprint, Flask, flash, redirect, url_for, session, render_template, request
from flask_login import login_required, current_user

from app import db
from model.produk import ProdukModel
from model.promo import PromoModel
from model.transaksi import TransaksiModel
from model.transaksidetail import TransaksiDetailModel
from datetime import datetime
from sqlite3 import IntegrityError

keranjang = Blueprint("keranjang", __name__, template_folder="templates", static_folder="static"
                      )
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'


def init_shopping_cart():
    if 'cart' not in session:
        session['cart'] = []


@keranjang.route('/customer/produk/add_to_cart/<id_produk>', methods=['POST'])
@login_required
def add_to_cart(id_produk):
    init_shopping_cart()

    produk = ProdukModel.query.get(id_produk)
    if produk:
        quantity = int(request.form.get('quantity'))
        available_stock = produk.stok  # Get the available stock for the product

        if quantity <= 0:
            flash('Jumlah produk harus lebih dari 0', 'danger')
            return redirect(url_for('produk.productpembeli'))
        if quantity <= available_stock:

            # Mengecek jika produk sudah ada di keranjang
            for item in session['cart']:
                if item['id_produk'] == produk.id_produk:
                    # Jika barang yang sama dimasukkan maka akan menambahkan quantity
                    if item['quantity'] + quantity <= available_stock:
                        promo = PromoModel.query.get(produk.id_promo)
                        item['quantity'] += quantity
                        if promo:
                            diskon_harga = produk.harga - (produk.harga * (promo.diskon / 100))
                            item['diskon_harga'] = diskon_harga
                            item['subtotal'] = diskon_harga * item['quantity']
                        else:
                            item['subtotal'] = item['harga'] * item['quantity']
                        flash('Produk quantity telah diperbarui', 'success')

                        # Kurangi stok yang tersedia
                        produk.stok -= quantity
                        db.session.commit()
                    else:
                        flash('Jumlah yang diminta melebihi stok yang tersedia', 'error')
                    break
            else:
                # Jika tidak ada di keranjang maka akan dimasukkan menjadi barang baru yang dimasukkan ke keranjang
                promo = PromoModel.query.get(produk.id_promo)

                if produk.id_promo is not None:
                    diskon_harga = produk.harga - (produk.harga * (promo.diskon / 100))
                    if promo:
                        subtotal = diskon_harga * quantity
                    else:
                        subtotal = produk.harga * quantity
                else:
                    subtotal = produk.harga * quantity

                # Cek apakah produk sudah ada di keranjang
                product_in_cart = False
                for item in session['cart']:
                    if item['id_produk'] == produk.id_produk:
                        product_in_cart = True
                        break

                if not product_in_cart:
                    item = {
                        'id_produk': produk.id_produk,
                        'harga': produk.harga,
                        'nama_product': produk.nama_product,
                        'gambar': produk.gambar,
                        'diskon': promo.diskon if promo else None,
                        'quantity': quantity,
                        'diskon_harga': diskon_harga if promo else 0,
                        'subtotal': subtotal
                    }
                    session['cart'].append(item)

                    flash('Produk sudah ditambahkan ke keranjang', 'success')
        else:
            flash('Stok produk tidak mencukupi', 'danger')
        return redirect(url_for('produk.productpembeli'))
    else:
        flash('Produk tidak ada', 'danger')

    return redirect(url_for('keranjang.cart'))


@keranjang.route('/customer/produk/cart')
@login_required
def cart():
    if current_user.role.role_name == 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard_page.dashboard'))
    active_page = 'cart'
    init_shopping_cart()
    cart = session['cart']
    # Jika keranjang masih kosong
    if not cart:
        flash('Keranjang Anda kosong. Silakan tambahkan produk terlebih dahulu.', 'info')
        return redirect(url_for('produk.productpembeli'))
    total = sum(item['subtotal'] for item in session['cart'])

    return render_template('user/cart.html', cart=cart, total=total, active_page=active_page)


@keranjang.route('/customer/cart/remove_from_cart/<id_produk>', methods=['POST'])
@login_required
def remove_from_cart(id_produk):
    # Mengambil id_produk yang akan dihapus dari keranjang
    produk_id_to_remove = id_produk

    # Mencari produk dalam keranjang dan menghapusnya
    for item in (session['cart']):
        if item['id_produk'] == produk_id_to_remove:
            # Mengembalikan stok ke produk setelah dihapus dari keranjang
            produk = ProdukModel.query.get(produk_id_to_remove)
            if produk:
                produk.stok += item['quantity']
                db.session.commit()

            # Menghapus item dari keranjang
            session['cart'].remove(item)

            flash('Produk berhasil dihapus dari keranjang', 'success')
            break
    else:
        flash('Produk tidak ditemukan dalam keranjang', 'danger')

    return redirect(url_for('keranjang.cart'))


@keranjang.route('/customer/cart/checkout', methods=['POST'])
@login_required
def checkout():
    if current_user.role.role_name == 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('dashboard_page.dashboard'))
    init_shopping_cart()

    user_id = current_user.id  # Replace with actual user ID
    date = datetime.now()
    total = sum(item['subtotal'] for item in session['cart'])

    transaksi = TransaksiModel(user_id=user_id, date=date, total=total)
    db.session.add(transaksi)
    db.session.commit()

    for item in session['cart']:
        detail_transaksi = TransaksiDetailModel(
            id_transaksi=transaksi.id_transaksi,
            id_produk=item['id_produk'],
            quantity=item['quantity'],
            subtotal=item['subtotal'],

        )
        db.session.add(detail_transaksi)
        db.session.commit()

        # Kurangkan stok produk
        produk = ProdukModel.query.get(item['id_produk'])
        if produk:
            produk.stok -= item['quantity']
            if produk.selling is None:
                produk.selling = item['quantity']
            else:
                produk.selling += item['quantity']
            db.session.commit()
        else:
            flash(f"Product with ID {item['id_produk']} not found.", 'danger')

    try:
        session.pop('cart')
        flash('Pembelian berhasil', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error dalam pembelian', 'danger')

    return redirect(url_for('dashboard.dashboarduser'))
