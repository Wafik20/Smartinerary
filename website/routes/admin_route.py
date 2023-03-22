#ADMIN ROUTE
#CONTAINS CRUD OPERATIONS ON CITY, ACTIVITY, ITENIRRARY ENTITIES WHICH ARE ONLY ADMIN ACCESSIBLE. 
# THINGS TO FIX:
# 					1- Don't forget to enforce login by @login_required, and checking if current user is admin before every request
#						on this route
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from flask import abort
from ..models import User, City, Activity, Itinerary, Smartinerary
import json
import random
from flask import request


admin_router = Blueprint('admin_router', __name__)

##CITIES 
#--------------------------------------------------------------------------
# Get all cities
@admin_router.route('/city/', methods=['GET'])
def get_all_cities():
	return jsonify([
		{
			'id': city.id, 'name': city.name, 'state': city.state
			} for city in City.query.all()
	])


# Create city
@admin_router.route('/city/', methods=['POST'])
#@login_required
def create_city():
	#if (current_user.is_admin == False):  return abort(401, "your are not authorized")
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
		'name': city.name,
		'state': city.state,
	 	'success': 'city has been deleted succesfully' 
	 }
#--------------------------------------------------------------------------


#ACTIVITIES
#--------------------------------------------------------------------------
# Add Activity
@admin_router.route('/activity/', methods=['POST'])
def create_activity():
	data = request.get_json()
	# enforce activity type, name, location
	if not 'activity_type' in data or not 'activity_place' in data or not 'activity_location' in data:
		return jsonify({
			'error': 'Bad Request',
			'message': 'invalid activity_type, activity_place, activity_location'
		}), 400
	# find the city by name (include city_name as the city name in the JSON request)
	city = City.query.filter_by(name=data['city_name']).first()
	# if there is no associated city return bad request
	if not city:
		return jsonify({
			'error': 'Bad request',
			'message': 'Invalid city'
		}), 400
	activity = Activity(
		city_id = city.id,
		#Type of activity
		# Activities may be morning, afternoon or evening
		activity_type = data['activity_type'],
		activity_action = data['activity_action'],
		activity_place = data['activity_place'],
		activity_location = data['activity_location'],
		activity_description = data['activity_description']
	)
	db.session.add(activity)
	db.session.commit()
	return {
		'activity_type': activity.activity_type, 'activity_place': activity.activity_place, 
		'activity_location': activity.activity_location, 'city': city.name
	}, 201
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Get activities
@admin_router.route('/activity/', methods=['GET'])
def get_activity():  # sourcery skip: avoid-builtin-shadow
	#only 3 valid types of activities (morning, afternoon, evening)
	# 
	valid_types = ['morning', 'afternoon', 'evening', "all"]
	#choose type
	type = request.args.get('type')
	#choose city
	city_name = request.args.get('city')
	city = City.query.filter_by(name=city_name).first_or_404()
	random_act = random.choice(list(Activity.query.filter_by(activity_type=type, city_id=city.id)))
	print({
		"act type": random_act.activity_type,
		"act city":	random_act.city_id
	})
	print(random_act)
	print(type)
	if type not in valid_types:
		return jsonify({
			'error': 'Bad request',
			'message': 'Invalid type of activity'
		}), 400
	if type == "all":
		return jsonify([
		{
		'id': activity.id, 'activity_type': activity.activity_type, 'activity_place': activity.activity_place, 
		'activity_location': activity.activity_location, 'city_id': activity.city_id
			} for activity in Activity.query.all()
	])
	return jsonify([
		{
		'id': activity.id, 'activity_type': activity.activity_type, 'activity_place': activity.activity_place, 
		'activity_location': activity.activity_location, 'city_id': activity.city_id
			} for activity in Activity.query.filter_by(activity_type=type, city_id=city.id)
	])
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#Get random activity with specified city and type
@admin_router.route('/activity_rand/', methods=['GET'])
def get_rand_activity():  # sourcery skip: avoid-builtin-shadow
	#only 3 valid types of activities (morning, afternoon, evening)
	# 
	valid_types = ['morning', 'afternoon', 'evening']
	#choose type
	type = request.args.get('type')
	#choose city
	city_name = request.args.get('city')
	#enforce city validity
	city = City.query.filter_by(name=city_name).first_or_404()
	#enforce type validity
	if type not in valid_types:
		return jsonify({
			'error': 'Bad request',
			'message': 'Invalid type of activity'
		}), 400
	#generate random activity based on the city and type
	activity_rand = random.choice(list(Activity.query.filter_by(activity_type=type, city_id=city.id)))
	return jsonify(
		{
		'id': activity_rand.id, 'activity_type': activity_rand.activity_type, 'activity_place': activity_rand.activity_place, 
		'activity_location': activity_rand.activity_location, 'city_id': activity_rand.city_id
			} 
	)
#---------------------------------------------------------------------------------------------------------------
# Iteniraries
# Create Itinerary (contains 3 activities)
#
@admin_router.route('/itinerary/', methods=['POST'])
def get_itinerary():
	#bind the itinerary to a Smartinerary
	smart_id = request.args.get('smart_id')
	
	#enfore Smartinerary validity
	smart = Smartinerary.query.filter_by(id=smart_id).first_or_404("Smartinerary not found")

	#choose city
	city_name = request.args.get('city')

	#enforce city validity
	city = City.query.filter_by(name=city_name).first_or_404("City not found")

	#get random morning activity
	morning_rand = random.choice(list(Activity.query.filter_by(activity_type="morning", city_id=city.id)))

	#get random afternoon activity
	afternoon_rand = random.choice(list(Activity.query.filter_by(activity_type="afternoon", city_id=city.id)))

	#get random evening activity
	evening_rand = random.choice(list(Activity.query.filter_by(activity_type="evening", city_id=city.id)))

	#create Itinerary
	itinerary = Itinerary(
		smart_itinerary_id = smart_id,
		morning_activity_id = morning_rand.id,
    	afternoon_activity_id = afternoon_rand.id,
    	evening_activity_id = evening_rand.id
	)
	db.session.add(itinerary)
	db.session.commit()
	return jsonify(
		{
		'id': itinerary.id, 'smartinerary_id': itinerary.smart_itinerary_id,
		'morning_activity': {
		'id': morning_rand.id, 'activity_type': morning_rand.activity_type, 'activity_place': morning_rand.activity_place, 
		'activity_location': morning_rand.activity_location, 'city_id': morning_rand.city_id
			},
		'afternoon_activity': {
		'id': afternoon_rand.id, 'activity_type': afternoon_rand.activity_type, 'activity_place': afternoon_rand.activity_place, 
		'activity_location': afternoon_rand.activity_location, 'city_id': afternoon_rand.city_id
			},
		'evening_activity': {
		'id': evening_rand.id, 'activity_type': evening_rand.activity_type, 'activity_place': evening_rand.activity_place, 
		'activity_location': evening_rand.activity_location, 'city_id': evening_rand.city_id
			} 
			} 
	)
# #------------------------------------------------------------------------------------------------------------------