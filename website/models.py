from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)


    # Define relationships
    smart_itineraries = relationship('Smartinerary', backref='user', lazy=True)

# class Smartinerary(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     name = db.Column(db.String(100))
#     description = db.Column(db.String(1000))

#     # Define relationships
#     itineraries = relationship('Itinerary', backref='smartinerary', lazy=True)
class Smartinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    # Define relationships
    itineraries = relationship('Itinerary', backref='smartinerary', lazy=True)

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    smart_itinerary_id = db.Column(db.Integer, db.ForeignKey('smartinerary.id'), nullable=False)
    morning_activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    afternoon_activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    evening_activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    activity_type = db.Column(db.String(100))
    activity_action = db.Column(db.String(100))
    activity_place = db.Column(db.String(100))
    activity_location = db.Column(db.Integer)
    activity_description = db.Column(db.String(1000))

    # Define relationships
    city = relationship('City', backref='activities', lazy=True)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    state = db.Column(db.String(100))