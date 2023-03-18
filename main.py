from flask import Flask, request, render_template, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from models.db_init import db
from models.User import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' #sets database
app.config['SQLALCHEMY_BINDS'] = {
    'destinations': 'sqlite:///destinations.db'
} 

#userdb = SQLAlchemy(app)
# init the dbs
db.init_app(app)


app.secret_key = 'development key'

@app.cli.command('initdb')
def initdb_command():

    db.drop_all()
    db.create_all()
    db.session.commit()

    print('Initialized the database.')


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
            session['username'] = user.username
            return redirect(url_for('mainpage', username = user.username))

    return render_template('login.html', error = error) # returns login template

@app.route('/register', methods=['GET', 'POST']) # staff registration page
def register():
    error = ""
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
            db.session.add(User(u, p)) # adds new user to db
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', error = error)

@app.route('/main_<username>', methods=['GET', 'POST'])
def mainpage(username):
    if (session['username']) is None:
        return redirect(url_for('login'))
    return render_template('mainpage.html', name = username)
