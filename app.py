from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_jsglue import JSGlue
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

from models.user import Users

jsglue = JSGlue()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'static/images'
    app.config.from_mapping(
        SECRET_KEY="Flamboyant Bakery",
        SQLALCHEMY_DATABASE_URI="sqlite:///flamboyant.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # route admin
    from routes.admin.dashboard import dashboard_page
    from routes.admin.kategori import kategori_page
    from routes.admin.produk import produk_page
    from routes.admin.promo import promo_page
    from routes.admin.transaksi import transaksi_page
    from routes.admin.input_promo import input_promo_page
    from routes.admin.customer import customer_page

    # route user
    from routes.user.dashboard import dashboard
    from routes.user.produk import produk
    from routes.user.cart import keranjang
    from routes.user.transaksi import transaksi

    # route guest
    from routes.guest.dashboard import landing
    from routes.guest.produk import g_prod
    from routes.guest.akun import g_auth

    # register route admin
    app.register_blueprint(dashboard_page)
    app.register_blueprint(kategori_page)
    app.register_blueprint(produk_page)
    app.register_blueprint(promo_page)
    app.register_blueprint(transaksi_page)
    app.register_blueprint(input_promo_page)
    app.register_blueprint(customer_page)

    # register route user
    app.register_blueprint(dashboard)
    app.register_blueprint(produk)
    app.register_blueprint(keranjang)
    app.register_blueprint(transaksi)

    # register route guest
    app.register_blueprint(landing)
    app.register_blueprint(g_prod)
    app.register_blueprint(g_auth)

    db.init_app(app)
    jsglue.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "g_auth.login"

    @login_manager.user_loader
    def loader_user(user_id):
        return Users.query.get(user_id)

    return app
