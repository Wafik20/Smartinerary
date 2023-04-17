## Smartinerary Routes
## Need to add: 1- filter by city 2-
##

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import User, Smartinerary, Itinerary, Activity, City
import json, random

smartinerary_router = Blueprint('smartinerary_router', __name__)

##----- SMARTINERARY -----------------
#User creates a smartinerary
@smartinerary_router.route('/', methods=['POST'])
@login_required
def create_smartinerary():
    data = request.form.to_dict()

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
        user_id=user.id,
        city_id=data['city_id'],
        name=data['name'],
        description=data['description']
    )
    db.session.add(smartinerary)
    db.session.commit()

    itinerary_list = []

    lenOfStay = data['lenOfStay']

    # enforce Smartinerary validity
    smart = Smartinerary.query.filter_by(
        id=smartinerary.id).first_or_404("Smartinerary not found")

    # choose city
    city_id = data['city_id']

    # enforce city validity
    city = City.query.filter_by(id=city_id).first_or_404("City not found")

    # get morning acts for city
    morning_acts = list(Activity.query.filter_by(activity_type="Morning", city_id=city.id))

    # get afternoon acts for city
    afternoon_acts = list(Activity.query.filter_by(activity_type="Afternoon", city_id=city.id))

    # get eve acts for city
    evening_acts = list(Activity.query.filter_by(activity_type="Evening", city_id=city.id))

    # choose three random morning activities
    morning_rand = random.sample(morning_acts, k=int(lenOfStay))

    # choose three random afternoon activities
    afternoon_rand = random.sample(afternoon_acts, k=int(lenOfStay))

    # choose three random evening activities
    evening_rand = random.sample(evening_acts, k=int(lenOfStay))

    # create Itinerary
    for day in range(int(lenOfStay)):
        morning = morning_rand[day]
        afternoon = afternoon_rand[day]
        evening = evening_rand[day]
        itinerary = Itinerary(
            smart_itinerary_id=smart.id,
            morning_activity_id=morning.id,
            afternoon_activity_id=afternoon.id,
            evening_activity_id=evening.id
        )
        itinerary_string = {
            'morning_activity': {
                'id': morning.id,
                'activity_type': morning.activity_type,
                'activity_action': morning.activity_action,
                'activity_place': morning.activity_place,
                'activity_location': morning.activity_location,
                'activity_description': morning.activity_description,
                "activity_image": morning.activity_image
            },
            'afternoon_activity': {
                'id': afternoon.id,
                'activity_type': afternoon.activity_type,
                'activity_action': afternoon.activity_action,
                'activity_place': afternoon.activity_place,
                'activity_location': afternoon.activity_location,
                'activity_description': afternoon.activity_description,
                 "activity_image": afternoon.activity_image
            },
            'evening_activity': {
                'id': evening.id,
                'activity_type': evening.activity_type,
                'activity_action': evening.activity_action,
                'activity_place': evening.activity_place,
                'activity_location': evening.activity_location,
                'activity_description': evening.activity_description,
                 "activity_image": evening.activity_image
            }
        }
        itinerary_list.append(itinerary_string)
        db.session.add(itinerary)
        db.session.commit()

    return render_template("smart.html", user = current_user, smartinerary = itinerary_list)

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#Get Smart
# Get a user's Smartinerary by ID
@smartinerary_router.route('/', methods=['GET'])
@login_required
def get_smartinerary():
    smart_id = request.args.get("smart_id")
    # get user
    user = current_user
    
    # get Smartinerary
    smart = Smartinerary.query.filter_by(id=smart_id, user_id=user.id).first_or_404("Smartinerary not found")

    itinerary_list = []

    # get Itinerary
    itineraries = Itinerary.query.filter_by(smart_itinerary_id=smart.id).all()

    for itinerary in itineraries:
        morning = Activity.query.get(itinerary.morning_activity_id)
        afternoon = Activity.query.get(itinerary.afternoon_activity_id)
        evening = Activity.query.get(itinerary.evening_activity_id)

        itinerary_string = {
            'morning_activity': {
                'id': morning.id,
                'activity_type': morning.activity_type,
                'activity_action': morning.activity_action,
                'activity_place': morning.activity_place,
                'activity_location': morning.activity_location,
                'activity_description': morning.activity_description,
                'activity_image': morning.activity_image
            },
            'afternoon_activity': {
                'id': afternoon.id,
                'activity_type': afternoon.activity_type,
                'activity_action': afternoon.activity_action,
                'activity_place': afternoon.activity_place,
                'activity_location': afternoon.activity_location,
                'activity_description': afternoon.activity_description,
                'activity_image': afternoon.activity_image
            },
            'evening_activity': {
                'id': evening.id,
                'activity_type': evening.activity_type,
                'activity_action': evening.activity_action,
                'activity_place': evening.activity_place,
                'activity_location': evening.activity_location,
                'activity_description': evening.activity_description,
                'activity_image': evening.activity_image
            }
        }
        itinerary_list.append(itinerary_string)

    return render_template("smart.html", user=current_user, smartinerary=itinerary_list)


#--------------------------------------------------------------------------------------------------
## Get all
## Get all smarts for the current user
@smartinerary_router.route('/user_smarts', methods=['GET'])
@login_required
def get_all_user_smartineraries():
    user_smarts = list(current_user.smart_itineraries)
    return render_template("user_smarts.html", user_smarts=user_smarts, user=current_user, is_admin = bool(current_user.is_admin))
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#Shuffle Itinerary for a user's Itinerary
@smartinerary_router.route('/shuffle', methods=['PUT'])
@login_required
def shuffle():
    
    return
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#Delete Smart and their corrosponding Itineraries
@smartinerary_router.route('/delete/', methods=['DELETE'])
def delete_smart():
    smart_id = request.args.get("smart_id")
    smartinerary = Smartinerary.query.filter_by(id=smart_id).first_or_404()
    smart_itineraries = Itinerary.query.filter_by(smart_itinerary_id=smart_id).all()
    for itin in smart_itineraries:
         db.session.delete(itin)
    
    db.session.delete(smartinerary)
    db.session.commit()
    return jsonify({
		'smart_id': smartinerary.id,
		'user_id': smartinerary.user_id, 'city_id': smartinerary.city_id, 
		'name': smartinerary.name, 'description': smartinerary.description
	})
