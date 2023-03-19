from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from flask import abort
from ..models import User, City
import json

admin_router = Blueprint('admin_router', __name__)

# Get all cities
@admin_router.route('/city/', methods=['GET'])
def get_users():
	return jsonify([
		{
			'id': city.id, 'name': city.name, 'email': city.state
			} for city in City.query.all()
	])


# Add city
@admin_router.route('/city/', methods=['POST'])
@login_required
def add_city():
	if (current_user.is_admin == False):  return abort(401, "your are not authorized")
	data = request.get_json()
	if not 'name' in data or not 'state' in data:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name of todo or email of creator not given'
		}), 400
	else:
		city = City(name = data['name'], state = data['state'])
		db.session.add(city)
		db.session.commit()
		return {
		'id': city.id, 'name': city.name, 
		'state': city.state 
	    }, 201
	
# Delete city
@admin_router.route('/city/<id>/', methods=['DELETE'] )
def delete_city(id):
	city = City.query.filter_by(id=id).first_or_404()
	db.session.delete(city)
	db.session.commit()
	return {
		'success': 'Data deleted successfully'
	}