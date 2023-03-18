from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import User
import json

home_router = Blueprint('home_router', __name__)


@home_router.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user = current_user)