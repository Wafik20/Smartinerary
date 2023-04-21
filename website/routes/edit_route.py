# EDIT PROFILE ROUTE: This route is responsible for editing the user profile, including password change.
# CONTAINS EDIT PROFILE FUNCTIONALITY: The route contains the edit_profile function that executes the password change functionality.

from .. import db
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask import request
from ..models import User
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Creating a Blueprint instance for the edit profile route
edit_router = Blueprint('edit_router', __name__)

# Defining the route for the edit profile functionality and the HTTP request methods it accepts
@edit_router.route('/', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        # Getting the old password, new password, and confirmation of the new password from the form submission
        old_pass = request.form['password1']
        new_pass = request.form['password2']
        new_pass_confirm = request.form['password3']
        
        # Validating the old password
        if not check_password_hash(current_user.password, old_pass):
            flash('Old password is incorrect', category='error')
        # Checking if the old and new passwords are same
        elif old_pass == new_pass:
            flash('Old Password cannot be new password', category='error')
        # Checking if the new passwords match
        elif new_pass != new_pass_confirm:
            flash("Passwords don't match", category='error')
        # Checking if the new password is of valid length
        elif len(new_pass) < 7:
            flash('New password must be at least 7 characters.', category='error')
        else:
            # Querying the user object from the database and setting its password to the new password
            temp = User.query.filter_by(id = current_user.id).first()
            temp.password = generate_password_hash(new_pass, method='sha256')

            # Committing the changes to the database
            db.session.commit()

            # Flashing a success message after the password change
            flash('Password successfully changed')
            
    # Rendering the edit_profile.html template with the user and is_admin variables
    return render_template('edit_profile.html', user=current_user, is_admin = bool(current_user.is_admin))
