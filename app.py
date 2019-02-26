from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = "soooo-secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()



#root directory
@app.route('/')
def redirect_to_register():
    '''redirect user to register a new account'''
    return redirect('/register')


#register directory
@app.route('/register', methods =["GET", "POST"])
def show_register_form():
    '''display registration form and handle new user registration'''
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/secret')
    else:
        return render_template('registration_form.html', form=form)


#login
@app.route('/login', methods =['GET','POST'])
def show_login_form():
    '''display login form and handle user login'''

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        current_user = User.authenticate(username, password)
        if current_user:
            session['user_id'] = current_user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Bad name/password']
    else:
        return render_template('login_form.html', form=form)


@app.route("/users/<username>")
def display_user_info(username):
    '''Display user information on login.'''

    if 'user_id' not in session:
        flash('You must be logged in to view!')
        return redirect("/")
    else:
        return render_template('secret.html',username=username)


#logout
@app.route('/logout', methods =['POST'])
def logout_user():
    ''' Log user out'''
    session.pop('user_id')
    return redirect('/')
    




