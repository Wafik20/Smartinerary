from flask import Flask, request, render_template, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' #sets database
userdb = SQLAlchemy(app)
app.secret_key = 'development key'

@app.cli.command('initdb')
def initdb_command():

    userdb.drop_all()
    userdb.create_all()

    userdb.session.commit()

    print('Initialized the database.')

class User(userdb.Model): # user class is username, password, and saved smartineraries
    username = userdb.Column(userdb.String(20), unique=True, primary_key=True)
    password = userdb.Column(userdb.String(20))
    savedSmartineraries = userdb.Column(userdb.__dict__)
    
    def __init__(self, username, password, savedSmartineraries):
        self.username = username
        self.password = password
        self.savedSmartineraries = savedSmartineraries
        
    def __repr__(self):
        return '<User %r %r' % (self.username, self.password, self.savedSmartineraries) # for debug purposes

class Smartinerary():
    def __init__(self, numdays, itineraries):
        self.numdays = numdays
        self.itineraries = itineraries


class Itinerary():
    def __init__(self, morning, afternoon, evening):
        self.morning = morning
        self.afternoon = afternoon
        self.evening = evening

    # def shuffle(timeOfDay):



@app.route('/', methods=['GET', 'POST'])
def login():
    session.clear()
    error = ""
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['user']).first()
        password = User.query.filter_by(password=request.form['pass']).first()
        
        if user is None:
            error = 'Invalid username'
        elif password is None:
            error = 'Invalid password'
        else: 
            abort(418)

    return render_template('login.html', error = error) # returns login template

@app.route('/register', methods=['GET', 'POST']) # staff registration page
def register():
    error = ""
    success = ""
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        p2 = request.form['password2']
        if not u:
            error = 'You have to enter a username'
        elif not p:
            error = 'You have to enter a password'
        elif p != p2:
            error = "Passwords don't match"
        elif User.query.filter_by(username = u).first() is not None: # makes sure usernames are unique
            error = 'The username is already taken'
        else:
            userdb.session.add(User(u, p)) # adds new user to db
            userdb.session.commit()
            success = 'New account added successfully'
            return redirect(url_for('login'))
    return render_template('register.html', error = error, success = success)
