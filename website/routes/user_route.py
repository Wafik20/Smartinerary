## USER ROUTES: CRUD OPERATION ON USER MODULE
## Added until now: GET, UPDATE, GET ALL
##
##
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import User
import json

user_route = Blueprint('user_route', __name__)


#get all users
@user_route.route('/')
@login_required
def get_users():
	
    if (current_user.is_admin == True):
        return jsonify([{'id': user.id, 'name': user.first_name, 'email': user.email, 'is admin': user.is_admin } for user in User.query.all()])
    else:
        return jsonify(['message: you are not authorized']), 401

#get user
@user_route.route('/<id>/')
@login_required
def get_user(id):
	print(id)
	user = User.query.filter_by(id=id).first_or_404()
	return {
		'id': user.id, 'name': user.first_name, 
		'email': user.email, 'is admin': user.is_admin
		}

#update user
## you have to include "first_name" in json request
@user_route.route('/<id>/', methods=['PUT'])
def update_user(id):
	data = request.get_json()
	if 'first_name' not in data:
		return {
			'error': 'Bad Request',
			'message': 'Name field needs to be present'
		}, 400
	user = User.query.filter_by(id=id).first_or_404()
	user.first_name=data['first_name']
	if 'is_admin' in data:
		user.is_admin=data['is_admin']
	if 'email' in data:
		user.email=data['email']
	db.session.commit()
	return jsonify({
		'id': user.id, 
		'name': user.first_name, 'is_admin': user.is_admin,
		'email': user.email
		})

#delete user