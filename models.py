# Import settings

from flask_sqlalchemy import SQLAlchemy

#------------------------------------------------

#PATH_DB = 'sqlite:////home/km/Dropbox/Git_Local/00 - Python/FlaskRestAlchemy/UserApi'

#----------------------------------

# create the sqlalchemy object

db = SQLAlchemy()

# database colums
#Id, timestamp, location_lat, location_long
#    timestamp BLOB,
#    location_lat NUMERIC,
#    location_long NUMERIC)
#                          ''')
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id',db.Integer,primary_key=True)
    username = db.Column('username',db.String(28),index=True, nullable = False,unique=True )
    timestamp = db.Column(db.DateTime)
    savedplaces = db.relationship('SavedPlaces',backref='user',lazy='dynamic')

    #def __init__(self,timestamp,username):
    #    self.timestamp = timestamp
    #    self.username = username

    def __repr__(self):
        return '<User %r>' % (self.username)


class SavedPlaces(db.Model):
    __tablename__='savedplaces'
    id = db.Column('id',db.Integer,primary_key=True)
    timestamp = db.Column(db.DateTime)
    location_lat = db.Column('location_lat',db.String(100),index = True, nullable = False)
    location_long = db.Column('location_long',db.String(100),index = True, nullable = False)
    waitingtime = db.Column('waitingtime',db.Integer, index= True )
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<SavedPlaces %r>' % (self.location_lat)




    #def __init__(self,timestamp,locaiton_lat, location_long):
    #    self.timestamp = timestamp
    #    self.location_lat = locaiton_lat
    #    self.location_long = location_long


# Inserting data
# Using Method Post
#-------------------------------------------

# post save location

# if location is near 50 m of favotire place, then be able to post waiting time
# receive location, query database for previsous location or just post wait time and save as favorite
# post waiting time


