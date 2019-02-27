from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, User, FeedBack
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from forms import RegistrationForm, LoginForm, AddFeedback, UpdateFeedback
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
        session['user_id']=username
        return redirect(f"/users/{username}")
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
        user = User.query.get(username)
        feedback = user.feedback_items
        return render_template('secret.html',username=username, feedback=feedback)


#logout
@app.route('/logout', methods =['POST'])
def logout_user():
    ''' Log user out'''
    session.pop('user_id')
    return redirect('/')


#add feedback
@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    ''' add feedback from user'''
    if 'user_id' not in session:
        flash('You must be logged in to view!')
        return redirect("/")

    form = AddFeedback()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = FeedBack(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f'/users/{username}')
    else:
        return render_template('add_feedback.html', username=username, form=form)


@app.route('/users/<username>/delete')
def delete_user(username):
    '''Delete user'''
    if 'user_id' not in session or session['user_id'] != username:
        flash('You are not authorized to view!')
        return redirect("/")
    user = User.query.get(username)
    user_posts = user.feedback_items
    for row in user_posts:
        db.session.delete(row)
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id')
    return redirect('/')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    ''' Render and process form for updating feedback'''
    if 'user_id' not in session:
        flash('You are not authorized to view!')
        return redirect("/")

    feedback = FeedBack.query.get(feedback_id)
    user = feedback.user
    form = UpdateFeedback(obj=feedback)
    
    if form.validate_on_submit():
        feedback.title=form.title.data
        feedback.content=form.content.data
        db.session.commit()

        return redirect(f'/users/{user.username}')
    else:
        return render_template('edit_feedback_form.html', feedback_id=feedback_id, form=form)


@app.route('/feedback/<int:feedback_id>/delete')
def delete_feedback(feedback_id):
    '''Delete feedback'''
    if 'user_id' not in session:
        flash('You are not authorized to view!')
        return redirect("/")
    feedback = FeedBack.query.get(feedback_id)
    user = feedback.user
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{user.username}')