from flask import render_template, flash, redirect, request
from flask_login import login_user, logout_user, login_required

from app import app, db
from models import User, Valve, Tank, TankValve

from werkzeug.security import generate_password_hash, check_password_hash

from collections import defaultdict

@app.route("/")
@login_required
def index():
    valves = Valve.query.all()
    valves_dict = defaultdict(list)

    for valve in valves:
        key = valve.location
        available_percentage = Tank.query.filter_by(id=TankValve.query.filter_by(valve_id=valve.id).first().tank_id).first().available_percentage
        valves_dict[key].append([valve.valve_no, valve.status, available_percentage])

    return render_template("index.html", valves=valves_dict)


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

        tank = Tank.query.filter_by(location=location).first()

        if tank is None:
            tank = Tank(location=location, available_percentage=100)
            db.session.add(tank)
            db.session.commit()

        tank_valve = TankValve(tank_id=tank.id, valve_id=valve.id)
        db.session.add(tank_valve)

        db.session.commit()

        return redirect('/valve')
    

@app.route('/valve-delete', methods=['POST'])
@login_required
def valve_delete(): 
    location = request.form.get('location')
    valve_no = request.form.get('valve_no')

    valve = Valve.query.filter_by(location=location, valve_no=valve_no).first()
    tank_valve = TankValve.query.filter_by(valve_id=valve.id).first()

    db.session.delete(valve)
    db.session.commit()

    db.session.delete(tank_valve)
    db.session.commit()

    valve_left_in_location = Valve.query.filter_by(location=location).first()

    if valve_left_in_location is None:
        tank = Tank.query.filter_by(location=location).first()
        print('deleting tank', tank)
        db.session.delete(tank)
        db.session.commit()

    return redirect('/valve')


@app.route('/valve-switch-status', methods=['POST'])
def switch_valve():
    location = request.form.get('location')
    valve_no = request.form.get('valve_no')

    valve = Valve.query.filter_by(location=location, valve_no=valve_no).first()

    tank = Tank.query.filter_by(id=TankValve.query.filter_by(valve_id=valve.id).first().tank_id).first()

    if valve.status == 0:

        if tank.available_percentage > 0:
            valve.status = 1
            db.session.commit()

            flash('Valve turned on with avilable water {}'.format(tank.available_percentage), category='success')

        else:
            flash('Tank is empty', category='warning')

    else:
        valve.status = 0
        db.session.commit()

        flash('Valve turned off remaining water {}'.format(tank.available_percentage), category='success')

    return redirect('/')


@app.route('/tank', methods=['GET'])
def tank():
    if request.method == 'GET':
        tanks = Tank.query.all()

        tanks_dict = defaultdict(list)

        for tank in tanks:
            key = tank.location
            tanks_dict[key].append([tank.id, tank.available_percentage])

        return render_template('tank.html', tanks=tanks_dict)