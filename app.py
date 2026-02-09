import os

from flask import Flask, render_template, flash

app = Flask(__name__)
app.secret_key = str(os.environ.get('SECRET_KEY'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')