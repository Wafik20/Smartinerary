# EDIT PROFILE ROUTE
# CONTAINS EDIT PROFILE FUNCTIONALITY

from .. import db
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask import request
from ..models import User
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

edit_router = Blueprint('edit_router', __name__)


@edit_router.route('/', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        old_pass = request.form['password1']
        new_pass = request.form['password2']
        new_pass_confirm = request.form['password3']
        if not check_password_hash(current_user.password, old_pass):
            flash('Old password is incorrect', category='error')
        elif old_pass == new_pass:
            flash('Old Password cannot be new password', category='error')
        elif new_pass != new_pass_confirm:
            flash("Passwords don't match", category='error')
        elif len(new_pass) < 7:
            flash('New password must be at least 7 characters.', category='error')
        else:
            temp = User.query.filter_by(id = current_user.id).first()
            temp.password = generate_password_hash(new_pass, method='sha256')

            db.session.commit()

            flash('Password successfully changed')
    #print(current_user.password)
    return render_template('edit_profile.html', user=current_user)