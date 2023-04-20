from flask import render_template, redirect, request, session, flash
from app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

from app.models.login import User
from app.models.sighting import Sighting


@app.route('/create/sighting')
def new_sighting():
    return render_template('create.html', user = User.get_user(session['user_id']))


@app.route('/save/sighting', methods= ['POST'])
def save_sighting():
    if not Sighting.validate_new_sighting(request.form):
        return redirect('/create/sighting')
    
    sighting_info = {
        'location' : request.form['location'],
        'describe_sighting' : request.form['describe_sighting'],
        'num_of_squatch' : request.form['num_of_squatch'],
        'user_id' : session['user_id'],
    }
    
    Sighting.add_sighting(sighting_info)
    print("   HERE   ", sighting_info) 
    return redirect('/dashboard')

@app.route('/update/sighting/<int:id>')
def update_sighting(id):
    
    if not 'user_id' in session:
        return redirect('/')
    
    sighting = Sighting.get_a_sighting({'id': id})
    
    if sighting and sighting.user_id == int(session['user_id']):      
        return render_template('edit.html', user = User.get_user(session['user_id']), sightings = sighting)
    
    return redirect('/dashboard')

@app.route('/update/sighting', methods=['POST'])
def save_update_sighting():

    sighting_to_update = Sighting.get_a_sighting_to_update(request.form)  
    
    if sighting_to_update:
        
        Sighting.update_sighting({
            'location' : request.form['location'],
            'describe_sighting' : request.form['describe_sighting'],
            'num_of_squatch' : request.form['num_of_squatch'],
            'user_id' : session['user_id'],
        })
    print(sighting_to_update)
    return redirect('/dashboard')

@app.route('/delete/sighting/<int:id>')
def delete_sighting(id):
    
    Sighting.delete_sighting(id)
    return redirect('/dashboard')

@app.route('/show/sighting/<int:id>')
def show_recipe(id):
    
    return render_template('show.html', user = User.get_user(session['user_id']), sightings = Sighting.get_a_sighting({'id': id}), )
