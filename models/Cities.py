from flask_sqlalchemy import SQLAlchemy
from models.db_init import db

class Cities(db.Model):
    __tablename__ = 'Cities'
    CityId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CityName = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), default='US')

    def __repr__(self):
        return f"<City {self.CityName}>"