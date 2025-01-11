from datetime import datetime
from flask import render_template, redirect, session, request, flash
from my_app.models.sighting import Sighting
from my_app.models.skeptic import Skeptic
from my_app.models.believer import Believer
from my_app.models.user import User  
from my_app import app

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.find_user_by_id(session['user_id'])  
    sightings = Sighting.get_all_sightings()
    return render_template('dashboard.html', user=user, sightings=sightings)

@app.route('/report_sighting', methods=['GET', 'POST'])
def report_sighting():
    if 'user_id' not in session:
        return redirect('/login')
    
    user = User.find_user_by_id(session['user_id'])

    if request.method == 'POST':
        data = {
            'location': request.form['location'],
            'date_of_sighting': request.form['date_of_sighting'],
            'number_of_sasquatches': request.form['number_of_sasquatches'],
            'description': request.form['description'],
            'reported_by': session['user_id']
        }
        
        # Validate that the date of sighting is in the past
        date_of_sighting = datetime.strptime(data['date_of_sighting'], '%Y-%m-%d')
        if date_of_sighting >= datetime.now():
            flash("The date of the sighting must be in the past.", 'danger')
            return render_template('report_sighting.html', user=user, data=data)
        
        # Validate that the number of Sasquatches is greater than 0
        if int(data['number_of_sasquatches']) <= 0:
            flash("The number of Sasquatches must be greater than 0.", 'danger')
            return render_template('report_sighting.html', user=user, data=data)
        
        Sighting.create_sighting(data)
        flash('Sighting reported successfully!', 'success')
        return redirect('/dashboard')
    
    return render_template('report_sighting.html', user=user)

@app.route('/sighting/<int:sighting_id>/edit', methods=['GET', 'POST'])
def edit_sighting(sighting_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    sighting = Sighting.get_sighting_by_id(sighting_id)
    user = User.find_user_by_id(session['user_id'])
    
    if request.method == 'POST':
        data = {
            'id': sighting_id,
            'location': request.form['location'],
            'date_of_sighting': request.form['date_of_sighting'],
            'number_of_sasquatches': request.form['number_of_sasquatches'],
            'description': request.form['description']
        }
        
        # Validate that the date of sighting is in the past
        date_of_sighting = datetime.strptime(data['date_of_sighting'], '%Y-%m-%d')
        if date_of_sighting >= datetime.now():
            flash("The date of the sighting must be in the past.", 'danger')
            return render_template('edit_sighting.html', user=user, sighting=sighting, data=data)
        
        # Validate that the number of Sasquatches is greater than 0
        if int(data['number_of_sasquatches']) <= 0:
            flash("The number of Sasquatches must be greater than 0.", 'danger')
            return render_template('edit_sighting.html', user=user, sighting=sighting, data=data)
        
        Sighting.update_sighting(data)
        flash('Sighting updated successfully!', 'success')
        return redirect('/dashboard')
    
    return render_template('edit_sighting.html', user=user, sighting=sighting)

@app.route('/sighting/<int:sighting_id>/skeptic', methods=['POST'])
def mark_as_skeptic(sighting_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    data = {
        'user_id': session['user_id'],
        'sighting_id': sighting_id
    }
    
    if Skeptic.mark_as_skeptic(data):
        flash("Marked as skeptical.", 'success')
    else:
        flash("You have already marked this sighting as skeptical.", 'danger')
    
    return redirect(request.referrer)

@app.route('/sighting/<int:sighting_id>/believer', methods=['POST'])
def mark_as_believer(sighting_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    data = {
        'user_id': session['user_id'],
        'sighting_id': sighting_id
    }
    
    if Believer.mark_as_believer(data):
        flash("Marked as believer.", 'success')
    else:
        flash("You have already marked this sighting as a believer.", 'danger')
    
    return redirect(request.referrer)

@app.route('/sighting/<int:sighting_id>/delete', methods=['POST'])
def delete_sighting(sighting_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    Sighting.delete_sighting(sighting_id)
    return redirect('/dashboard')

@app.route('/sighting/<int:sighting_id>/view')
def view_sighting(sighting_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    user = User.find_user_by_id(session['user_id'])
    sighting = Sighting.get_sighting_by_id(sighting_id)
    
    data = {
        'user_id': session['user_id'],
        'sighting_id': sighting_id
    }
    
    has_marked_as_skeptic = Skeptic.has_marked_as_skeptic(data)
    has_marked_as_believer = Believer.has_marked_as_believer(data)
    
    return render_template('view_sighting.html', user=user, sighting=sighting, has_marked_as_skeptic=has_marked_as_skeptic, has_marked_as_believer=has_marked_as_believer)