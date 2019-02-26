
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


class User(db.Model):
    '''user class'''
    __tablename__ = 'users'

    username = db.Column(db.String(20), 
                         primary_key=True)

    password = db.Column(db.Text, 
                         nullable=False)

    email = db.Column(db.String(50), 
                      nullable=False)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                           nullable=False)