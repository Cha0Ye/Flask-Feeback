
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


class User(db.Model):
    '''user class'''
    __tablename__ = 'users'