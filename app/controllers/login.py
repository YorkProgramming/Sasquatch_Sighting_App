from flask import render_template, redirect, request, session, flash
from app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

from app.models.login import User
from app.models.sighting import Sighting




@app.route('/')
def home():
    return render_template('register.html')

@app.route('/create/user', methods= ['POST'])
def create_user():
    
    if not User.validate_registration(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    user_info = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash,
    }
    
    session['user_id'] =  User.add_user(user_info)
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    
    email = request.form['email']
    password = request.form['password']
    
    user = User.get_by_email(email)

    if user and bcrypt.check_password_hash(user.password, password):
        
        session['user_id'] = user.id
        return redirect('/dashboard')
    
    else:
        return redirect('/')


@app.route('/dashboard')
def dashboard():
    
    if not 'user_id' in session:
        return redirect('/')
    
    user_id = {'id': session["user_id"]}
    print(user_id)
    return render_template('dashboard.html', user = User.get_user(session['user_id']), sightings = Sighting.get_all_sightings())

@app.route('/logout')
def logout():
    session.pop('user_id')
    
    return redirect('/')