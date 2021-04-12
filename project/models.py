from flask_login import UserMixin
from . import db
from datetime import datetime
from hashlib import sha256

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    admin = db.Column(db.Boolean(), default=False)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    size = db.Column(db.String(20))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    hashed_name = db.Column(db.String(300))

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.hashed_name = sha256(
            name.encode('utf-8')).hexdigest()
