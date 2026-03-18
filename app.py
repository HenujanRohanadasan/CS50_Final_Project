import os

from flask import Flask
from flask_login import LoginManager

from models import db, User

app = Flask(__name__)
app.secret_key = str(os.environ.get('SECRET_KEY'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

import routes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))