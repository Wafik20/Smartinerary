## Smartinerary Routes
## Need to add: 1- filter by city 2-
##

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import User, Smartinerary
import json

smartinerary_router = Blueprint('smartinerary_router', __name__)

##----- SMARTINERARY -----------------
#User creates a smartinerary
@smartinerary_router.route('/', methods=['POST'])
@login_required
def create_smartinerary():
	data = request.get_json()
	# enforce city_id
	if not 'city_id' in data:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Smartinerary is not referenced to a valid city'
		}), 400
	# get user
	user = current_user
	# create smartinerary
	smartinerary = Smartinerary(
		user_id = user.id,	
		city_id = data['city_id'],
		name = data['name'],
		description = data['description']
	)
	db.session.add(smartinerary)
	db.session.commit()
	return {
		'id': smartinerary.id,
		'user_id': smartinerary.user_id, 'city_id': smartinerary.city_id, 
		'name': smartinerary.name, 'description': smartinerary.description
	}, 201

## Get all
## Get all itineraries for the current user
@smartinerary_router.route('/', methods=['GET'])
@login_required
def get_all_smartineraries():
	curr_user_id = current_user.id
	return jsonify([
		{ 
			'id': smartinerary.id,
            'user_id': smartinerary.user_id, 'city_id': smartinerary.city_id, 
		    'name': smartinerary.name, 'description': smartinerary.description 
		} for smartinerary in Smartinerary.query.filter_by(user_id=curr_user_id)
        ])