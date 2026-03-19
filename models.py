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
    valve_no = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)


class Tank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80), nullable=False)
    available_percentage = db.Column(db.Float, nullable=False)


class TankValve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tank_id = db.Column(db.Integer, db.ForeignKey('tank.id'), nullable=False)
    valve_id = db.Column(db.Integer, db.ForeignKey('valve.id'), nullable=False)


class ValveLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valve_id = db.Column(db.Integer, db.ForeignKey('valve.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)