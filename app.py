import os

from flask import Flask, render_template, flash, redirect, request
from flask_session import Session
from flask_login import LoginManager, login_required, logout_user, login_user
from models import db, User

from werkzeug.security import generate_password_hash, check_password_hash

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':

        user_name = request.form.get('username')
        password = request.form.get('password')

        if (user_name == '') or (password == ''):
            flash('Please enter both username and password', category='warning')
            return redirect('/login')
        
        user = User.query.filter_by(user_name=user_name).first()

        if user is None:
            flash('Incorrect username', category='warning')
            return redirect('/login')
        
        if check_password_hash(user.password, password) == False:
            flash('Incorrect password', category='warning')
            return redirect('/login')
        
        login_user(user, remember=True)
        
        return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register(): 
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST':

        user_name = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if (user_name == '') or (password == '') or (password_confirm == ''):
            flash('Please enter both username and password', category='warning')
            return redirect('/register')
        
        if password != password_confirm:
            flash('Passwords do not match', category='warning')
            return redirect('/register')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters', category='warning')
            return redirect('/register')
        
        user = User.query.filter_by(user_name=user_name).first()

        if user is not None:
            flash('Username already taken', category='warning')
            return redirect('/register')
        

        user = User(user_name=user_name, password=generate_password_hash(password))

        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)

        return redirect('/')


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')