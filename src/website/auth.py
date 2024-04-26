from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
# hash a password
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # this is how you get or see data from the database
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
        

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get('email') #
        user_name = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=user_name).first()

        if user_email:
            flash('Email already exists.', category='error')
        if user_username:
            flash('Username already exists.', category='error')
        elif len(email) < 4:
            flash('Email must me greater than 3 characters', category='error')
        elif len(user_name) < 2:
            flash('First name must me greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters.', category='error')
        else:
            # add user to the database
            new_user = User(email=email, username=user_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            

    return render_template('sign_up.html', user=current_user)

@auth.route("/change_username", methods=['GET', 'POST'])
@login_required
def change_username():
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        user = User.query.filter_by(username=new_username).first()
        
        if len(new_username) < 1:
            flash('Username must be at least 1 character.', category='error')
        if user:
            flash('Username Already Exists', category='error')
        else:
            current_user.username = new_username
            db.session.commit()
            flash('Username updated successfully!', category='success')
            return redirect(url_for('views.profile'))
    return render_template("change_username.html")

@auth.route("/change_email", methods=['GET', 'POST'])
@login_required
def change_email():
    if request.method == 'POST':
        new_email = request.form.get('new_email')
        user = User.query.filter_by(email=new_email).first()
        if user:
            flash('Email Already Exists', category='error')
        else:
            current_user.email = new_email
            db.session.commit()
            flash('Email updated successfully!', category='success')
            return redirect(url_for('views.profile'))
    return render_template("change_email.html")

@auth.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect', category='error')
        elif new_password != confirm_password:
            flash('New passwords don\'t match', category='error')
        elif len(new_password) < 8:
            flash('New password must be at least 8 characters.', category='error')
        else:
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            current_user.password = hashed_password
            db.session.commit()
            flash('Password changed successfully!', category='success')
            return redirect(url_for('views.quiz'))  # Changed here
            
    return render_template("change_password.html")