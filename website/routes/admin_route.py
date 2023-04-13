# ADMIN ROUTE
# CONTAINS CRUD OPERATIONS ON CITY, ACTIVITY, ITENIRRARY ENTITIES WHICH ARE ONLY ADMIN ACCESSIBLE.
# THINGS TO FIX:
# 					1- Don't forget to enforce login by @login_required, and checking if current user is admin before every request
# on this route
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .. import db
from flask import abort
from ..models import User, City, Activity, Itinerary, Smartinerary
import json
import random
from flask import request


admin_router = Blueprint('admin_router', __name__)


def get_cities():
    print(City.query.all())
    return list(City.query.all())


def get_activities():
    print(Activity.query.all())
    return list(Activity.query.all())

def get_users():
    print(User.query.all())
    return list(User.query.all())
# Go to admin dashboard:

@admin_router.route('/')
def admin_dashboard():
    return render_template('admin_dash.html', user=current_user, cities=get_cities(), activities=get_activities(), users=get_users())

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# toggle admin status
@admin_router.route('/user/<int:user_id>/toggle_admin', methods=['POST'])
@login_required
def toggle_admin(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    user.is_admin = not user.is_admin
    db.session.commit()
    return jsonify({"user_id": user_id,
                    "first_name": user.first_name,
                    "email": user.email,
                    "is_admin": user.is_admin
                    })


# CITIES
# --------------------------------------------------------------------------
# Get all cities


@admin_router.route('/city/', methods=['GET'])
def get_all_cities():
    return jsonify([
        {
            'id': city.id, 'name': city.name, 'state': city.state
        } for city in City.query.all()
    ])


# Create city
@admin_router.route('/city', methods=['POST'])
# @login_required
def create_city():
    # if (current_user.is_admin == False):  return abort(401, "your are not authorized")
    name = request.form["city_name"]
    state = request.form["state"]
    new_city = City(name=name, state=state)
    db.session.add(new_city)
    db.session.commit()
    # return render_template()
    print(name, state)
    return redirect("/admin")

# Delete city


@admin_router.route('/city', methods=['DELETE'])
def delete_city():
    city_id = request.args.get('city_id')
    city = City.query.filter_by(id=city_id).first_or_404()
    db.session.delete(city)
    db.session.commit()
    return {
        'name': city.name,
        'state': city.state,
        'success': 'city has been deleted succesfully'
    }
# --------------------------------------------------------------------------


# ACTIVITIES
# --------------------------------------------------------------------------
# Add Activity
@admin_router.route('/activity/', methods=['POST'])
def create_activity():
    city_id = request.form["city_id"]
    activity_type = request.form["activity_type"]
    activity_action = request.form["activity_action"]
    activity_place = request.form["activity_place"]
    activity_location = request.form["activity_location"]
    activity_description = request.form["activity_description"]
    # find the city by name (include city_name as the city name in the JSON request)
    city = City.query.filter_by(id=city_id).first()
    # if there is no associated city return bad request
    if not city:
        return jsonify({
            'error': 'Bad request',
            'message': 'Invalid city'
        }), 400
    activity = Activity(
        city_id=city.id,
        # Type of activity
        # Activities may be morning, afternoon or evening
        activity_type=activity_type,
        activity_action=activity_action,
        activity_place=activity_place,
        activity_location=activity_location,
        activity_description=activity_description
    )
    db.session.add(activity)
    db.session.commit()
    return redirect("/admin")
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# Get activities


@admin_router.route('/activity/', methods=['GET'])
def get_activity():  # sourcery skip: avoid-builtin-shadow
    # only 3 valid types of activities (morning, afternoon, evening)
    #
    valid_types = ['morning', 'afternoon', 'evening', "all"]
    # choose type
    type = request.args.get('type')
    # choose city
    city_name = request.args.get('city')
    city = City.query.filter_by(name=city_name).first_or_404()
    random_act = random.choice(
        list(Activity.query.filter_by(activity_type=type, city_id=city.id)))
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
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
# Get random activity with specified city and type


@admin_router.route('/activity_rand/', methods=['GET'])
def get_rand_activity():  # sourcery skip: avoid-builtin-shadow
    # only 3 valid types of activities (morning, afternoon, evening)
    #
    valid_types = ['morning', 'afternoon', 'evening']

    # choose type
    type = request.args.get('type')

    # choose city
    city_name = request.args.get('city')

    # enforce city validity
    city = City.query.filter_by(name=city_name).first_or_404()

    # enforce type validity
    if type not in valid_types:
        return jsonify({
            'error': 'Bad request',
            'message': 'Invalid type of activity'
        }), 400

    # generate random activity based on the city and type
    activity_rand = random.choice(
        list(Activity.query.filter_by(activity_type=type, city_id=city.id)))
    return jsonify(
        {
            'id': activity_rand.id, 'activity_type': activity_rand.activity_type, 'activity_place': activity_rand.activity_place,
            'activity_location': activity_rand.activity_location, 'city_id': activity_rand.city_id
        }
    )
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
# Delete Activity


@admin_router.route('/activity/', methods=['DELETE'])
def delete_activity():
    activity_id = request.args.get('activity_id')
    activity = Activity.query.filter_by(id=activity_id).first_or_404()
    db.session.delete(activity)
    db.session.commit()
    return jsonify(
        {
            'id': activity.id, 'activity_type': activity.activity_type, 'activity_place': activity.activity_place,
            'activity_location': activity.activity_location, 'city_id': activity.city_id
        }
    )


# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
# Iteniraries
# Create Itinerary (contains 3 activities)
#
@admin_router.route('/itinerary', methods=['POST'])
def get_itinerary():
    # bind the itinerary to a Smartinerary
    data = request.get_json()

    smart_id = data['smart_id']

    # enforce Smartinerary validity
    smart = Smartinerary.query.filter_by(
        id=smart_id).first_or_404("Smartinerary not found")

    # choose city
    city_id = data['city_id']

    # enforce city validity
    city = City.query.filter_by(id=city_id).first_or_404("City not found")

    # get random morning activity
    morning_rand = random.choice(
        list(Activity.query.filter_by(activity_type="Morning", city_id=city.id)))

    # get random afternoon activity
    afternoon_rand = random.choice(
        list(Activity.query.filter_by(activity_type="Afternoon", city_id=city.id)))

    # get random evening activity
    evening_rand = random.choice(
        list(Activity.query.filter_by(activity_type="Evening", city_id=city.id)))

    # create Itinerary
    itinerary = Itinerary(
        smart_itinerary_id=smart_id,
        morning_activity_id=morning_rand.id,
        afternoon_activity_id=afternoon_rand.id,
        evening_activity_id=evening_rand.id
    )
    db.session.add(itinerary)
    db.session.commit()
    smart_res = jsonify(
        {
            'id': itinerary.id, 'smartinerary_id': itinerary.smart_itinerary_id,
            'activities': [
                {
                    'id': morning_rand.id, 'activity_type': morning_rand.activity_type, 'activity_place': morning_rand.activity_place,
                    'activity_location': morning_rand.activity_location, 'city_id': morning_rand.city_id,
                    'activity_time': 'morning'
                },
                {
                    'id': afternoon_rand.id, 'activity_type': afternoon_rand.activity_type, 'activity_place': afternoon_rand.activity_place,
                    'activity_location': afternoon_rand.activity_location, 'city_id': afternoon_rand.city_id,
                    'activity_time': 'afternoon'
                },
                {
                    'id': evening_rand.id, 'activity_type': evening_rand.activity_type, 'activity_place': evening_rand.activity_place,
                    'activity_location': evening_rand.activity_location, 'city_id': evening_rand.city_id,
                    'activity_time': 'evening'
                }
            ]
        }
    )
    return  render_template('smart.html', user = current_user, smartinerary = smart_res) 

# #------------------------------------------------------------------------------------------------------------------
