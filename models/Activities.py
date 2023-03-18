from flask_sqlalchemy import SQLAlchemy
from models.db_init import db

class Activities(db.Model):
    __tablename__ = 'Activities'
    ActivityId = db.Column(db.Integer, primary_key=True)
    CityId = db.Column(db.Integer, db.ForeignKey('Cities.CityId'), nullable=False)
    ActivityPlace = db.Column(db.String(50))
    ActivityName = db.Column(db.String(50))
    ActivityType = db.Column(db.String(50), nullable=False)
    ActivityLocation = db.Column(db.String(50))
    ActivityDescription = db.Column(db.String(250))

    city = db.relationship('Cities', backref='activities')

    def __repr__(self):
        return f"<Activity {self.ActivityName}>"