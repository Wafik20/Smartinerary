from flask_sqlalchemy import SQLAlchemy
from models.db_init import db   

class User(db.Model):
    username = db.Column(db.String(20), unique=True, primary_key=True)
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r %r' % (self.username, self.password) # for debug purposes