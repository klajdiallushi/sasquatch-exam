from flask import render_template, redirect, session, request, flash
from my_app.models.user import User
from flask_bcrypt import Bcrypt
from my_app import app

bcrypt = Bcrypt(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/dashboard')
    
    if request.method == 'POST':
        user = User.find_user_by_email(request.form)
        if isinstance(user, str): 
            flash(f"Error: {user}", 'error')
            return redirect(request.referrer)
        if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Invalid email or password.', 'loginError')
            return redirect(request.referrer)
        session['user_id'] = user.id
        return redirect('/dashboard')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect('/dashboard')
    
    if request.method == 'POST':
        if User.find_user_by_email(request.form):
            flash('This email already exists. Try another one.', 'emailSignUp')
            return redirect(request.referrer)

        if not User.validate_user(request.form):
            return redirect(request.referrer)

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password']),
            'confirm_password': request.form['confirm_password']
        }
        User.create_user(data)
        flash('User successfully created. Please log in.', 'userRegister')
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
