# Import settings

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import os

# ------------------------
# debug imports
import datetime



# To generate the database
#
# from server import app
#
# """Connect the database to our Flask app."""
# # create the sqlalchemy db
# curDir = os.getcwd()  # current working dir
#
# PATH_DB = 'sqlite:///' + curDir + '/CheckzDB'
#
# # Configure to use our database
# app.config['SQLALCHEMY_DATABASE_URI'] = PATH_DB
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)


# ----------------------------------
db = SQLAlchemy()
# ----------------------------------
# Database Mapper
# ----------------------------------



class User(db.Model):
    """    Model Table User    """
    __tablename__ = 'user'

    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String, unique=True, nullable=False)
    pw_hash = db.Column('password_hash', db.String(80), nullable=False)
    username = db.Column('username', db.String(28), index=True, unique=True)
    created_timestamp = db.Column(db.String(28))
    savedplaces = db.relationship('SavedPlaces', backref='user')

    def __init__(self, email, pw_hash, username, created_timestamp):
        self.email = email
        self.pw_hash = generate_password_hash(pw_hash)
        self.created_timestamp = created_timestamp
        self.username = username

    def verify_password(self, password):
        """Verify user's password, a method that can be called on a user."""

        return check_password_hash(self.pw_hash, password)

    @property
    def serialize(self):
        return {'id': self.id,
                'username': self.username,
                'created_timestamp': self.created_timestamp}


# ------------------------------------------------------
# Second database Table
# ------------------------------------------------------
class SavedPlaces(db.Model):
    """
    Model Table SavedPlaces
    """
    __tablename__ = 'savedplaces'
    id = db.Column('id', db.Integer, primary_key=True)
    created_timestamp = db.Column(db.DateTime)
    modified_timestamp = db.Column(db.DateTime)
    location_lat = db.Column('location_lat', db.String(100))
    location_long = db.Column('location_long', db.String(100))
    address = db.Column('address', db.String(100))
    waiting_time = db.Column('waitingtime', db.Integer)
    type_location = db.Column('type_location', db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, created_timestamp, modified_timestamp, location_lat, location_long, address, waiting_time,
                 type_location, user_id):
        self.created_timestamp = created_timestamp
        self.modified_timestamp = modified_timestamp
        self.location_lat = location_lat
        self.location_long = location_long
        self.address = address
        self.waiting_time = waiting_time
        self.type_location = type_location
        self.user_id = user_id

    @property
    def serialize(self):
        #  Return as a json object
        return {'user_id': self.user_id,
                'created_timestamp': self.created_timestamp,
                'modified_timestamp': self.modified_timestamp,
                'location_lat': self.location_lat,
                'location_long': self.location_long,
                'address': self.address,
                'waiting_time': self.waiting_time,
                'type_location': self.type_location}


##############################################################################
# Helper functions

def connect_to_db(app):

    """Connect the database to our Flask app."""
    # create the sqlalchemy db
    #curDir = os.getcwd()  # current working dir

    curDir = os.path.abspath(os.path.dirname(__file__))

    PATH_DB = 'sqlite:///' + curDir + '/CheckzDB'

    # Configure to use our database
    app.config['SQLALCHEMY_DATABASE_URI'] = PATH_DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


def insert_user():
    email = "email@email.com"
    password = 123
    pending_user = "user"
    created_timestamp = datetime.datetime.utcnow()

    user = User(email=email, pw_hash=password, username=pending_user, created_timestamp=created_timestamp)

    current_session = db.session  # open database session
    current_session.add(user)  # add opened statement to opened session
    current_session.commit()  #

    print("insert_user was executed ")


if __name__ == "__main__":

    from checkz_app.server import app
    connect_to_db(app)
    #insert_user()
    print("Connected to DB.")
