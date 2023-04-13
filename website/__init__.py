# THE INIT FILE
# USED TO CREATE THE APP AND TO INIT THE DB. 


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin, current_user

#pre: Flask App is not init
#post: Flask App is init
db = SQLAlchemy()

#setting db name
DB_NAME = "database.db"

#pre: login view is not set, and db is not created and init
#post: db is created and routes are set, and login page
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .routes.user_route import user_route
    from .routes.home_route import home_router
    from .routes.admin_route import admin_router
    from .routes.smartineraries_route import smartinerary_router
    from .auth import auth

    app.register_blueprint(home_router, url_prefix='/')
    app.register_blueprint(user_route, url_prefix='/users')
    app.register_blueprint(admin_router, url_prefix='/admin')
    app.register_blueprint(smartinerary_router, url_prefix='/smartineraries')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#Create the db
#pre: db is not created
#post db is created
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
