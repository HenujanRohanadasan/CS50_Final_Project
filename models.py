from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Valve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80), nullable=False)
    zone = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)