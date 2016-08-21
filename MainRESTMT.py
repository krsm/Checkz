# Import settings
#   python3.5
import datetime

from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

import geofuntcions as gf
#from models import db, User, SavedPlaces
from schemas import ma,savedplace_schema,savedplaces_schema, user_schema,users_schema

# ----------------------
# Max distance btw 2 locations
# it will be to compare the distance
# it is in meters

RADIUS_CIRCLE = 10
RADIUS_SAVED_PLACES = 30000  # considering closed places in radius of 30km

# ------------------------------------------------

PATH_DB = 'sqlite:////home/km/Dropbox/Git_Local/00 - Python/FlaskRestAlchemy/UserApi'

app = Flask("MainRESTMT")
app.config['SQLALCHEMY_DATABASE_URI'] = PATH_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY']= os.urandom(24)    # will be used in the cookie - to encrypt the cookie


# initiate the sqlalchemy object

# db.init_app(app)

db = SQLAlchemy(app)




# Database Mapper
# ----------------------------------

class User(db.Model):
    """
    Model Table User
    """

    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(28), index=True, unique=True)
    created_timestamp = db.Column(db.String(28))
    savedplaces = db.relationship('SavedPlaces', backref='user')

    def __init__(self, created_timestamp, username):
        self.created_timestamp = created_timestamp
        self.username = username

    @property
    def serialize(self):
        '''Return as a json object so it can be used in RESTful Api'''

        return {'id': self.id,
                'username': self.username,
                'created_timestamp': self.created_timestamp}

# Second database Table


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, created_timestamp,modified_timestamp, location_lat, location_long, address, waiting_time, user_id):
        self.created_timestamp = created_timestamp
        self.modified_timestamp = modified_timestamp
        self.location_lat = location_lat
        self.location_long = location_long
        self.address = address
        self.waiting_time = waiting_time
        self.user_id = user_id

    @property
    def serialize(self):
        '''
        As a json object to be used in RESTful Api
        '''
        return {'user_id': self.user_id,
                'created_timestamp': self.created_timestamp,
                'modified_timestamp': self.modified_timestamp,
                'location_lat': self.location_lat,
                'location_long': self.location_long,
                'address': self.address,
                'waiting_time': self.waiting_time}




# ----------------------------------
# Inserting data
# Using Method Post
# -------------------------------------------

# ------------------------------------------------------
#  Endpoints related to User Table
@app.route('/create_user/', methods=['POST'])
def createuser():
    """
    :return:
    """

    if not request.json or not 'username' in request.json:
        abort(404)

    # getting json data
    content = request.get_json(force=True)
    # timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    created_timestamp = datetime.datetime.now()
    username = content["username"]

    # create object to insert in the database
    userdata = User(created_timestamp=created_timestamp, username=username)
    current_session = db.session  # ope database session

    try:
        current_session.add(userdata)  # add opened statement to opened session
        current_session.commit()  # commit changes
    except Exception as e:
        current_session.rollback()
        current_session.flush()  # for resetting non-commited .add()
        print(e)
    finally:
        current_session.close()

    users = User.query.filter_by(username=username).all()  # it was supposed to be first

    return jsonify(user_json=[user.serialize for user in users])

 # events = Events.query.filter_by(event_type = event_type).all()
#return jsonify(json_list = [event.serialize for event in events])


# GET user details
@app.route('/get_user/<username>', methods=['GET'])
def get_user_info(username):
    """
    Query data related to username ans return as a json object
    """
    users = User.query.filter_by(username=username).all()  # it was supposed to be first
    return jsonify(user_json=[User.serialize for user in users])


# Delete user
@app.route('/delete_user/<username>')
def delete_user(username):
    pass


# ----------------------------------------------
# Routes regarding SavedPlaces Table

# get all previous saved places

@app.route('/get_all_saved_places/', methods=['GET'])
def getallsavedplaces():
    """
    Query data related to all previous saved places and return as a json object

    """

    if request.method == 'GET':

        # code to update all waiting time columns
        # create function to update waiting time all rows

        #username = request.query_string
        username = request.args.get('username')
        current_location_lat = float(request.args.get('location_lat'))
        current_location_long = float(request.args.get('location_long'))

        allsavedplaces = SavedPlaces.query.filter_by(username=username).all()


        #users = User.query.filter_by(username=username).all()  # it was supposed to be first
        #return jsonify(user_json=[User.serialize for user in users])


       # if allsavedplaces is not None:

        return jsonify(savedplaces_json=[SavedPlaces.serialize for allsavedplace in allsavedplaces])
    #else:

     #   return 'Not GET method'

# - End of points related to User Table
# ------------------------------------------------------

@app.route('/create_save_place/', methods=['POST'])
def createsaveplace():
    """
    :return:
    """
    if not request.json or not 'location_lat' in request.json or not 'location_long' in request.json or not 'username' in request.json:
        abort(404)

    # parsing request data
    # -------------------------

    content = request.get_json(force=True)
    created_timestamp = datetime.datetime.now()
    modified_timestamp = datetime.datetime.now()
    username = content["username"]
    locationlat = content["location_lat"]
    locationlong = content["location_long"]
    waiting_time = content["waiting_time"]
    address = content["address"]

    # create object to insert in the database
    # prepare query statement

    # create query to confirm that username already exists in the table user
    # otherwise insert in the table

    current_session = db.session  # open database session

    owner_id = current_session.query(User).filter_by(username=username).first().username

    if owner_id is not None:
        savedplaces = SavedPlaces(created_timestamp=created_timestamp, modified_timestamp=modified_timestamp,
                                  location_lat=locationlat, location_long=locationlong,
                                  address=address, waiting_time=waiting_time, user_id=owner_id)
    try:
        # Verify if the location already exists

        # query previous locations save by the user
        # query_savedplaces = SavedPlaces.filter_by(username=jsonusername).all() # fetch all entries on the table

        # if query result is none, then value should be
        # if query_savedplaces is None:
        current_session.add(savedplaces)  # add opened statement to opened session
        current_session.commit()  # commit changes
    except Exception as e:
        current_session.rollback()
        current_session.flush()  # for resetting non-commited .add()
        print(e)
    finally:
        current_session.close()
    return "OK"


# ----------------------------------------------------------------------
# route to update the waiting time

@app.route('/update_saved_places/', methods=['POST'])
def updatesavedplaces():
    if not request.json or not 'location_lat' in request.json or not 'location_long' in request.json or not 'username' in request.json:
        abort(404)

    # parsing request data
    # -------------------------

    content = request.get_json(force=True)
    created_timestamp =  datetime.datetime.now()
    modified_timestamp = datetime.datetime.now()  # get a new data to update
    username = content["username"]
    locationlat = content["location_lat"]
    locationlong = content["location_long"]
    waiting_time = content["waiting_time"]
    address = content["address"]
    # ---------------------------

    current_session = db.session  # open database session

    # query places coordinates to see if the place already
    # query latitude
    # query longitude

    # query table USer to get username and then query by user
    owner_id = current_session.query(User).filter_by(username=username).first().username

    if owner_id is not None:

        querysavedplaces = current_session.query(SavedPlaces).filter_by(user_id=owner_id).all()

        if querysavedplaces is not None:

            # parsing query
            for location in querysavedplaces:
                # verify if the distance of the newlocation is already in the database, or if there is a close location
                # verifying that calculating distance of 2 points, it will be considered as same place if the distance btw 2 points is smaller than 10 m
                distance_location, same_location = gf.verify_distance(float(locationlat), float(locationlong),
                                                                      float(location.location_lat),
                                                                      float(location.location_long), RADIUS_CIRCLE)
                if same_location is True:
                    # keep the old location
                    # create average latitude and longitude?
                    # recreate this later
                    # ---------------------------
                    location.modified_stamp = modified_timestamp
                    # long = location.location_long
                    location.waiting_time = waiting_time
                    # user_id = location.user_id
                    # address = location.address
                    # ---------------------------
                    # savedplaces = SavedPlaces(timestamp=timestamp, location_lat=locationlat, location_long=locationlong, waiting_time=waiting_time, user_id  =user_id)
                    # savedplaces = querysavedplaces
                    # break

                    #querysavedplaces.waiting_time = waiting_time
                    #querysavedplaces.timestamp = timestamp
                    # savedplaces = SavedPlaces(timestamp=timestamp, location_lat=locationlat, location_long=locationlong, waiting_time=waiting_time, user_id=owner_id)
                else:
                    pass
                    # create a new location
                    # savedplaces = SavedPlaces(timestamp=timestamp, location_lat=locationlat, location_long=locationlong, waiting_time=waiting_time, user_id  =owner_id)

    try:
        # current_sesssion.add(savedplaces) # add opened statement to opened session
        current_session.commit()  # commit changes

    except:
        current_session.rollback()
        current_session.flush()  # for resetting non-commited .add()
    finally:
        current_session.close()

    # return HTTP response
    # resp = jsonify()

    return "ok"


# catch page error
# ----------------------

# @app.errorhandler(404)
# def not_found(error):
#    return make_response(jsonify({'error': 'Not found'}), 404)
# -----------------------------
'''
#@app.before_request to run a function before every request from the browser:
@app.before_request
def before_request():
    db.session()

#@app.teardown_request to close the database connection after every request.
@app.teardown_request
def teardown_request(exception):
   db.session.remove()

#----------------------
'''
if __name__ == '__main__':
    app.run(debug=True)
