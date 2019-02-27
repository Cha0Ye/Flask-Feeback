from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, BooleanField, IntegerField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, NumberRange, URL

class RegistrationForm(FlaskForm):
    '''Form for adding new user'''
    username = StringField('Username:', 
                            validators=[InputRequired()])

    password = PasswordField('Password:', 
                            validators=[InputRequired()])

class LoginForm(FlaskForm):
    '''Form for user login'''
    
    username = StringField('Username:', 
                            validators=[InputRequired()])

    password = PasswordField('Password:', 
                            validators=[InputRequired()])


class AddFeedback(FlaskForm):
    ''' Form to add feedback given we know who the user is'''
    title = StringField('Title: ',
                         validators=[InputRequired()])

    content = TextAreaField('Content: ', 
                             validators=[InputRequired()])

class UpdateFeedback(FlaskForm):
    ''' Form to add feedback given we know who the user is'''

    title = StringField('Title: ',
                         validators=[InputRequired()])

    content = TextAreaField('Content: ', 
                             validators=[InputRequired()])