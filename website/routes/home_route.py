from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import User, Smartinerary, City
import json

home_router = Blueprint('home_router', __name__)

def get_cities():
    print(City.query.all())
    return list(City.query.all())

def get_user_smartineraries():
    print(list(current_user.smart_itineraries))
    return list(current_user.smart_itineraries)

def get_smartineraries():
    print(Smartinerary.query.all())
    return list(Smartinerary.query.all())
# Go to admin dashboard:

@home_router.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user = current_user, cities=get_cities(), user_smarts = get_user_smartineraries())