## Smartinerary Routes
## Need to add: 1- filter by city 2-
##

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import User, Smartinerary, Itinerary, Activity
import json

smartinerary_router = Blueprint('smartinerary_router', __name__)

def get_smartinerary_activities(smart_id):
    itinerary = Itinerary.query.filter_by(smart_itinerary_id=smart_id).first()
    morning_act = Activity.query.filter_by(id=itinerary.morning_activity_id).first()
    afternoon_act = Activity.query.filter_by(id=itinerary.afternoon_activity_id).first()
    evening_act = Activity.query.filter_by(id=itinerary.evening_activity_id).first()

    activities = []
    if morning_act:
        activities.append({
            "id": morning_act.id,
            "activity_type": morning_act.activity_type,
            "activity_action": morning_act.activity_action,
            "activity_place": morning_act.activity_place,
            "activity_location": morning_act.activity_location,
            "activity_description": morning_act.activity_description,
            "time_of_day": "morning"
        })
    if afternoon_act:
        activities.append({
            "id": afternoon_act.id,
            "activity_type": afternoon_act.activity_type,
            "activity_action": afternoon_act.activity_action,
            "activity_place": afternoon_act.activity_place,
            "activity_location": afternoon_act.activity_location,
            "activity_description": afternoon_act.activity_description,
            "time_of_day": "afternoon"
        })
    if evening_act:
        activities.append({
            "id": evening_act.id,
            "activity_type": evening_act.activity_type,
            "activity_action": evening_act.activity_action,
            "activity_place": evening_act.activity_place,
            "activity_location": evening_act.activity_location,
            "activity_description": evening_act.activity_description,
            "time_of_day": "evening"
        })

    return activities


##----- SMARTINERARY -----------------
#User creates a smartinerary
@smartinerary_router.route('/', methods=['POST'])
@login_required
def create_smartinerary():
	data = request.get_json()

	# enforce city_id
	if 'city_id' not in data:
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
		'smart_id': smartinerary.id,
		'user_id': smartinerary.user_id, 'city_id': smartinerary.city_id, 
		'name': smartinerary.name, 'description': smartinerary.description
	}, 201
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#Get Smart
@smartinerary_router.route('/', methods=['GET'])
@login_required
def get_smart():
	smart_id = request.args.get("smart_id")
	acts = get_smartinerary_activities(smart_id)
	return render_template("smart.html", user = current_user, activities = acts)

#--------------------------------------------------------------------------------------------------
## Get all
## Get all itineraries for the current user
@smartinerary_router.route('/getall', methods=['GET'])
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