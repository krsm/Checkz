# Import settings
#   python3.5
import datetime
import os

from flask import Flask, render_template, redirect, request, session, jsonify
from flask import abort, url_for

import geofuntcions as gf
from models import connect_to_db, db, User, SavedPlaces

#related to sqlalchemy

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func



# ----------------------
# Max distance btw 2 locations
# it will be to compare the distance
# it is in meters

RADIUS_CIRCLE = 3   # distance used to be same place in meters
RADIUS_SAVED_PLACES = 30000  # considering closed places in radius of 30km

# ------------------------------------------------

# Create a flask app and set a random secret key
# Create the app
app = Flask(__name__)
app.secret_key = os.urandom(24)


# raises error if you use an undefined variable in Jinja2
#app.jinja_env.undefined = StrictUndefined

# ================================================================================
#  Registration, Login, and User Profile
# ================================================================================
# @app.before_request
# def before_request():
#     g.user = None
#     if 'username' in session:
#         g.user = session['username']

@app.route('/register/', methods=['POST','GET'])
def register():
    error = None

    if request.method == 'POST':

        email = request.form.get('email')
        # check if the email was already used in the database
        pending_user_email = User.query.filter_by(email=email).first()

        if pending_user_email is not None:

            # Create function to inform that email was already used

            # pass error saying that email already in the database
            error = "Email already in the database, please, log in!"

            return redirect(url_for('login'))
        else:

            password = request.form['password']
            pending_user = request.form['username']
            created_timestamp = datetime.datetime.utcnow()

            user = User(email=email, pw_hash=password, username=pending_user, created_timestamp=created_timestamp)

            current_session = db.session  # open database session

            try:
                current_session.add(user)  # add opened statement to opened session
                current_session.commit()  # commit changes

                # initiate the session with the current user
                # create a user_id session
                session['user_id'] = user.id
                session['username'] = pending_user

            except:
                current_session.rollback()
                current_session.flush()  # for resetting non-commited .add()

                # In case of fail not start the session with
                session['user_id'] = None
                session['username'] = None

            finally:
                current_session.close()

        return render_template('map.html')
    else:
        #error = "405  Method not allowed"
        return render_template('register.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    current_session = db.session  # open database session
    error = None
    if request.method == 'POST':

        password = request.form['password']
        email = request.form['email']

        possible_user = User.query.filter_by(email=email).first()

        if possible_user and possible_user.verify_password(password):

            session['username'] = possible_user.username
            session['user_id'] = possible_user.id
            return render_template("map.html")

        else:
            error = "Invalid Credentials. Please try again."
            return render_template("login.html", error=error)

    else:
        # error = "405  Method not allowed"
        return render_template("login.html", error=error)

    current_session.close()

@app.route('/logout/')
def logout():
    session.pop('username', None)
    # this remove the entire session dictionary
    session.clear()
    return render_template("map.html")

# Homepage
@app.route('/')
def home():
    return render_template("map.html")


# ------------------------------------------------------
# ------------------------------------------------------
# Inserting data
# Using Method Post
# ------------------------------------------------------
# ------------------------------------------------------
#   Endpoints related to User Table
# ------------------------------------------------------
# get all previous saved places
@app.route('/get_favorite_places', methods=['GET'])
def get_all_favorite_places():
    """
    Query data related to all previous saved places and return as a json object

    """
    """

            #  Return as a json object
        return {'user_id': self.user_id,
                'created_timestamp': self.created_timestamp,
                'modified_timestamp': self.modified_timestamp,
                'location_lat': self.location_lat,
                'location_long': self.location_long,
                'address': self.address,
                'waiting_time': self.waiting_time,
                'type_location': self.type_location}


    """
    user_id = request.args.get('user_id')

    #if user_id is not None:

    current_session = db.session  # open database session

    # query all previous saved places for certain user

    #allsavedplaces = current_session.query(SavedPlaces).filter_by(user_id=user_id).all()

    allsavedplaces = SavedPlaces.query.filter_by(user_id=user_id).all()

    #TODO evaluate use the user current location to display just the saved places in a range closer to user current location

    saved_places = []

    if allsavedplaces is not None:

        for place in allsavedplaces:

            #if place.user_id:

            saved_places.append({'user_id': place.user_id,
                                 'created_timestamp': place.created_timestamp,
                                 'modified_timestamp': place.modified_timestamp,
                                 'location_lat': place.location_lat,
                                 'location_long': place.location_long,
                                 'address': place.address,
                                 'waiting_time': place.waiting_time,
                                 'type_location': place.type_location})

    current_session.close()

    # response = make_response(json.dumps(saved_places))
    #
    # response.content_type = "application/json"
    #
    # print(response)

    return jsonify({"saved_places": saved_places})
    #return response

    #TODO use @property method of class to serialize response
    #return jsonify(savedplaces_json=[SavedPlaces.serialize for allsavedplace in allsavedplaces])


# - End of points related to User Table
# ------------------------------------------------------
#   POST /create_save_place/ - create a new favorite place place in the database
@app.route('/save_favorite_place/', methods=['POST','GET'])
def save_favorite_place():
    """ Save user's favorite spot to db """
    #if not request.json or not 'location_lat' in request.json or not 'location_long' in request.json or not 'user_id' in request.json:
    #    abort(404)

    # parsing request data
    # -------------------------
    a = request
    #content = request.get_json(force=True)
    created_timestamp = datetime.datetime.now()
    modified_timestamp = datetime.datetime.now()
    user_id = request.form["user_id"]
    locationlat = request.form["location_lat"]
    locationlong = request.form["location_long"]
    #waiting_time = request.form["waiting_time"]
    type_location = request.form["type_location"]

    waiting_time = None
    #type_location = None
    #address = request.args.get("address")

    # to be improved and use google geocoding
    address = gf.get_location_address(locationlat, locationlong)

    # create object to insert in the database
    # prepare query statement

    # create query to confirm that username already exists in the table user
    # otherwise insert in the table

    current_session = db.session  # open database session
    username = current_session.query(User).filter_by(id=user_id).first().username

    if username is not None:

        querysavedplaces = current_session.query(SavedPlaces).filter_by(user_id=user_id).all()

        if querysavedplaces is not None:
            # parsing previous locations to confirm if it is unique the new entry
            for location in querysavedplaces:

                distance_location, same_location = gf.verify_distance(float(locationlat), float(locationlong),
                                                                      float(location.location_lat),
                                                                      float(location.location_long), RADIUS_CIRCLE)
                # if the user is inserting a place already saved, previous location will be kept,
                # and modified_stamp will be changed
                if same_location is True:
                    location.modified_timestamp = modified_timestamp
                    #update type_location
                    location.type_location = type_location
                    # then commit that change
                    try:
                        # current_session.add(querysavedplaces)  # add opened statement to opened session
                        current_session.commit()  # commit changes
                    except Exception as e:
                        current_session.rollback()
                        current_session.flush()  # for resetting non-commited .add()
                        print(e)
                    finally:
                        current_session.close()
                        return "OK modified timestamp update,type_location"  # exit function

        savedplaces = SavedPlaces(created_timestamp=created_timestamp, modified_timestamp=modified_timestamp,
                                  location_lat=locationlat, location_long=locationlong,
                                  address=address, waiting_time=waiting_time, type_location=type_location,
                                  user_id=user_id)
        try:
            current_session.add(savedplaces)  # add opened statement to opened session
            current_session.commit()  # commit changes
        except:
            current_session.rollback()
            current_session.flush()  # for resetting non-commited .add()
        finally:
            current_session.close()
            return "new_favorite_location_inserted"

# route to remove favorite place
@app.route('/remove_favorite_place', methods=['POST'])
def remove_favorite_place():
    """ Remove user's favorite spot to db """

    user_id = request.form.get('user_id')
    location_lat = request.form.get("location_lat")
    location_long = request.form.get("location_long")

    #current_session = db.session  # open database session

    #to_be_removed = current_session.query(SavedPlaces).filter_by(SavedPlaces.user_id == user_id, SavedPlaces.location_lat ==location_lat,
    #                                                         SavedPlaces.location_long == location_long).first()

    to_be_removed = SavedPlaces.query.filter(SavedPlaces.user_id == user_id, SavedPlaces.location_lat == location_lat,
                                             SavedPlaces.location_long == location_long).delete()

    #print(to_be_removed)

    if to_be_removed is not None:

        try:
            SavedPlaces.query.filter(SavedPlaces.user_id == user_id, SavedPlaces.location_lat == location_lat,
                                     SavedPlaces.location_long == location_long).delete()
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()  # for resetting non-commited .add()
        finally:
            db.session.close()

    return "Executed"
    #TODO finish query to see the lat and long and remove place from database


# route to get updated waiting time
# ----------------------------------------------------------------------
@app.route('/get_updated_waiting_time', methods=['GET'])
def get_updated_waiting_time():

    # parsing request data
    # -------------------------

    user_id = request.args.get('user_id')
    location_lat = request.args.get('location_lat')
    location_long = request.args.get('location_long')

    # ---------------------------
    current_session = db.session  # open database session

    # query table USer to get username and then query by user
    owner_name = current_session.query(User).filter_by(id=user_id).first().username

    if owner_name is not None:

        # get all saved places by all users
        #querysavedplaces = current_session.query(SavedPlaces).filter_by().all()

            #to_be_removed = SavedPlaces.query.filter(SavedPlaces.user_id == user_id, SavedPlaces.location_lat == location_lat,
             #                                SavedPlaces.location_long == location_long).delete()

        allsavedplaces = SavedPlaces.query.filter(SavedPlaces.user_id == user_id,SavedPlaces.location_lat == location_lat,
                                                  SavedPlaces.location_long == location_long).all()

        print(allsavedplaces)

        #TODO evaluate use the user current location to display just the saved places in a range closer to user current location

        saved_places = []

        if allsavedplaces is not None:

            for place in allsavedplaces:

                saved_places.append({'user_id': place.user_id,
                                     'created_timestamp': place.created_timestamp,
                                     'modified_timestamp': place.modified_timestamp,
                                     'location_lat': place.location_lat,
                                     'location_long': place.location_long,
                                     'address': place.address,
                                     'waiting_time': place.waiting_time,
                                     'type_location': place.type_location})

        current_session.close()

        # response = make_response(json.dumps(saved_places))
        #
        # response.content_type = "application/json"
        #
        # print(response)

        print(saved_places)

        return jsonify({"saved_places": saved_places})


# route to update the waiting time
@app.route('/update_waiting_time', methods=['POST'])
def update_waiting_time():


    # parsing request data
    # -------------------------

    user_id = request.form.get('user_id')
    location_lat = request.form.get('location_lat')
    location_long = request.form.get('location_long')
    waiting_time = request.form.get('updated_waiting_time')

    created_timestamp = datetime.datetime.now()
    modified_timestamp = datetime.datetime.now()  # get a new data to update

    # ---------------------------
    current_session = db.session  # open database session

    # query table USer to get username and then query by user
    owner_name = current_session.query(User).filter_by(id=user_id).first().username

    if owner_name is not None:

        # get all saved places by all users
        querysavedplaces = current_session.query(SavedPlaces).filter_by().all()

        if querysavedplaces is not None:

            # parsing query
            for location in querysavedplaces:
                # verify if the distance of the newlocation is already in the database, or if there is a close location
                # verifying that calculating distance of 2 points, it will be considered as same place if the distance btw 2 points is smaller than 10 m
                distance_location, same_location = gf.verify_distance(float(location_lat), float(location_long),
                                                                      float(location.location_lat),
                                                                      float(location.location_long), RADIUS_CIRCLE)
                if same_location is True:
                    location.modified_timestamp = modified_timestamp
                    location.waiting_time = waiting_time
                    try:
                        current_session.commit()  # commit changes
                    except:
                        current_session.rollback()
                        current_session.flush()  # for resetting non-commited .add()

    current_session.close()

    return "update_waiting_time_done"


# route to update the waiting time
@app.route('/get_direction_shortest_waiting_time', methods=['POST'])
def get_shortest_waiting_time():


    # parsing request data
    # -------------------------

    user_id = request.form.get('user_id')
    location_lat = request.form.get('location_lat')
    location_long = request.form.get('location_long')
    waiting_time = request.form.get('updated_waiting_time')
    type_location = request.form.get('type_location')

    created_timestamp = datetime.datetime.now()
    modified_timestamp = datetime.datetime.now()  # get a new data to update

    # ---------------------------
    current_session = db.session  # open database session
    # query table USer to get username and then query by user
    owner_name = current_session.query(User).filter_by(id=user_id).first().username

    if owner_name is not None:

           # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        # get all saved places by all users
        querysavedplaces = current_session.query(SavedPlaces).filter(user_id = user_id, type_location = type_location).\
            order_by(SavedPlaces.waiting_time)

        saved_places = {}

        if querysavedplaces is not None:

            for location in querysavedplaces:

                print(location.waiting_time,location.type_location)

                saved_places.append({'user_id': location.user_id,
                                     'created_timestamp': location.created_timestamp,
                                     'modified_timestamp': location.modified_timestamp,
                                     'location_lat': location.location_lat,
                                     'location_long': location.location_long,
                                     'address': location.address,
                                     'waiting_time': location.waiting_time,
                                     'type_location': location.type_location})

        current_session.close()

        # response = make_response(json.dumps(saved_places))
        #
        # response.content_type = "application/json"
        #
        # print(response)

        print(saved_places)

        return jsonify({"saved_places": saved_places})




    return


'''

# Delete saved place
@app.route('/delete_saved_place/', method = ['POST'])
def delete_saved_place():
    if not request.json or not 'location_lat' in request.json or not 'location_long' in request.json or not 'username' in request.json:
        abort(404)

    return "ok"



'''
# ----------------------


# # catch page error
# # ----------------------
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
# # -----------------------------

#lat = request.args.get('lat')
#long = request.args.get('long')

if __name__ == '__main__':


    connect_to_db(app)

    app.debug = True
    #pdb.set_trace()
    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    #app.run(host="192.168.1.110")
    app.run()