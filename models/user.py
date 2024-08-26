import uuid

from flask_bcrypt import Bcrypt
from flask_login import UserMixin

from app import db
from models.role import RoleModel
from models.status import StatusModel


class Users(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False, unique=True, default=lambda: uuid.uuid4().hex)
    email = db.Column(db.String)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    fullname = db.Column(db.String)
    usia = db.Column(db.Integer)
    alamat = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    role = db.relationship(RoleModel, foreign_keys=role_id)
    notelp = db.Column(db.String)
    id_status = db.Column(db.Integer, db.ForeignKey('status.id_status'))

    status = db.relationship(StatusModel, foreign_keys=id_status)

    def __int__(self, email, username, password, fullname, usia, alamat, role_id, notelp, id_status):
        self.email = email
        self.username = username
        self.password = Bcrypt.generate_password_hash(password).decode('utf-8')
        self.fullname = fullname
        self.usia = usia
        self.alamat = alamat
        self.role_id = role_id
        self.notelp = notelp
        self.id_status = id_status
