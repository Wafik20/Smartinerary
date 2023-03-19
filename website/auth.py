from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

#Problems:
# 1- Login and Sign-up has to work through the form, and does not work by sending a JSON request (does not work in postman).
# 2- 

#name of the blueprint
auth = Blueprint('auth', __name__)

#the login route
#pre: user is not logged in
#post: used is logged in or prompted that he does not have a valid acc
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ##FOR TESTING IN POSTMAN:
        # data = request.get_json()
        # email = data['email']
        # password = data['password']
        # print(email, password)
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home_router.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# logout route
# pre: user is logged in with a valid account
# post: user is not logged in anymore, and is prompted to the login page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# sign-up route
# pre: user is does not have an account
# post: user has an account and is stored in the database, and is prompted to his home page.
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            new_user.is_admin = False
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('home_router.home'))

    return render_template("sign_up.html", user=current_user)
