from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

from flask_wtf import FlaskForm
#from forms import AddNewPetForm, EditPetForm
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = "soooo-secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

user = User()

