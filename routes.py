from flask import render_template, flash, redirect, request
from flask_login import login_user, logout_user, login_required

from app import app, db
from models import User, Valve

from werkzeug.security import generate_password_hash, check_password_hash

from collections import defaultdict

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


@app.route('/valve', methods=['GET', 'POST'])
@login_required
def valve():
    if request.method == 'GET':
        valves = Valve.query.all()
        valves_dict = defaultdict(list)

        for valve in valves:
            key = valve.location
            valves_dict[key].append(valve.valve_no)

        return render_template('valve.html', valves=valves_dict)
    
    elif request.method == 'POST':

        location = request.form.get('location')
        valve_no = request.form.get('valve_no')

        if (location == '') or (valve_no == ''):    
            flash('Please fill location and valve number', category='warning')
            return redirect('/valve')
        
        elif valve_no.isnumeric() == False or int(valve_no) < 0:
            flash('Valve number must be a positive integer', category='warning')
            return redirect('/valve')
        
        
        valve = Valve.query.filter_by(location=location, valve_no=valve_no).first()

        if valve is not None:
            flash('Valve already exists', category='warning')
            return redirect('/valve')

        valve  = Valve(location=location, valve_no=valve_no, status=0)

        db.session.add(valve)
        db.session.commit()

        return redirect('/valve')
    

@app.route('/valve-delete', methods=['POST'])
@login_required
def valve_delete(): 
    location = request.form.get('location')
    valve_no = request.form.get('valve_no')

    valve = Valve.query.filter_by(location=location, valve_no=valve_no).first()

    db.session.delete(valve)
    db.session.commit()

    return redirect('/valve')