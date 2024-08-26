from app import db


class RoleModel(db.Model):
    __tablename__ = "role"
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, role_name):
        self.role_name = role_name
