from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import User
import json

smartinerary_router = Blueprint('smartinerary_router', __name__)