# -*- coding: utf-8 -*-

# Import settings

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

from .database import Base


# ------------------------
# debug imports

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
# db = SQLAlchemy()
# ----------------------------------
# Database Mapper
# ----------------------------------
class User(Base):

    """    Model Table User    """
    __tablename__ = 'user'

    id = Column('id', Integer, primary_key=True)
    email = Column('email', String, unique=True, nullable=False)
    pw_hash = Column('password_hash', String(80), nullable=False)
    username = Column('username', String(28), index=True, unique=True)
    created_timestamp = Column(String(28))
    savedplaces = relationship('SavedPlaces', backref=backref('user'))

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
class SavedPlaces(Base):
    """
    Model Table SavedPlaces
    """
    __tablename__ = 'savedplaces'
    id = Column('id', Integer, primary_key=True)
    created_timestamp = Column(DateTime)
    modified_timestamp = Column(DateTime)
    location_lat = Column('location_lat', String(100))
    location_long = Column('location_long', String(100))
    address = Column('address', String(100))
    waiting_time = Column('waitingtime', Integer)
    type_location = Column('type_location', String(100))
    user_id = Column(Integer, ForeignKey('user.id'))

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


