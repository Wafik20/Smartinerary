# Description: This file contains the route for the home page
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import User, Smartinerary, City
import json

# Create a blueprint for the home page
home_router = Blueprint('home_router', __name__)

# Home page route
@home_router.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user = current_user, is_admin = bool(current_user.is_admin))

