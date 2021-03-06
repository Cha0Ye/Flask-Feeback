from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    '''connect to db'''
    db.app = app
    db.init_app(app)


class User(db.Model):
    '''user class'''
    __tablename__ = 'users'

    username = db.Column(db.String(20), 
                         primary_key=True)

    password = db.Column(db.Text, 
                         nullable=False)

    # email = db.Column(db.String(50), 
    #                   nullable=False)

    # first_name = db.Column(db.String(30),
    #                        nullable=False)

    # _name = db.Column(db.String(30),
    #                        nullable=False)
    
    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)
        
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

class FeedBack(db.Model):
    '''FeedBack class'''
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer,
                   primary_key=True)

    title = db.Column(db.String(100),
                      nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    username = db.Column(db.Text,
                         db.ForeignKey('users.username'),
                         nullable=False)

    user = db.relationship('User', backref='feedback_items')

