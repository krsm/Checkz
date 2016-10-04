# Import settings
#   python3.5
import datetime
import os

from flask import Flask, request, jsonify, abort, render_template, session, redirect, url_for, g

import geofuntcions as gf
from models import connect_to_db, db, User, SavedPlaces

# ----------------------
# Max distance btw 2 locations
# it will be to compare the distance
# it is in meters

RADIUS_CIRCLE = 10
RADIUS_SAVED_PLACES = 30000  # considering closed places in radius of 30km

# ------------------------------------------------

# Create a flask app and set a random secret key
# Create the app
app = Flask(__name__)
app.secret_key = os.urandom(24)


# ================================================================================
#  Registration, Login, and User Profile
# ================================================================================


@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']


@app.route('/register/', methods=['POST', 'GET'])
def register():
    error = None

    if request.method == 'POST':

        email = request.form['email']
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
            except:
                current_session.rollback()
                current_session.flush()  # for resetting non-commited .add()
            finally:
                current_session.close()

            # initiate the session with the current user

            session['logged_in'] = True
            session['username'] = pending_user

            return render_template('map.html')
    else:

        # error = "405  Method not allowed"

        return render_template('register.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':

        password = request.form['password']
        email = request.form['email']

        possible_user = User.query.filter_by(email=email).first()

        if possible_user and possible_user.verify_password(password):
            session['username'] = possible_user.username
            session['logged_in'] = True
            return render_template("map.html")

        else:
            error = "Invalid Credentials. Please try again."
            return render_template("login.html", error=error)

    else:
        # error = "405  Method not allowed"
        return render_template("login.html", error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return render_template("map.html")


# function to verify the current is in the session
def verify_user_current_session():
    user = User.query.filter_by(name=session['username']).first()

    if user:
        return True
    else:
        return False


# Homepage
@app.route('/')
def home():
    # session['logged_in'] = True
    return render_template("map.html")


# ------------------------------------------------------
# ------------------------------------------------------
# Inserting data
# Using Method Post
# ------------------------------------------------------
# ------------------------------------------------------
#   Endpoints related to User Table
# ------------------------------------------------------
#   POST /create_user/ - create a new user
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
    user_data = User(created_timestamp=created_timestamp, username=username)
    current_session = db.session  # open database session

    try:
        current_session.add(user_data)  # add opened statement to opened session
        current_session.commit()  # commit changes
    except:
        current_session.rollback()
        current_session.flush()  # for resetting non-commited .add()
    finally:
        current_session.close()

    users = User.query.filter_by(username=username).all()  # it was supposed to be first

    return jsonify(user_json=[user.serialize for user in users])


# ------------------------------------------------------
# GET user details
@app.route('/get_user/<username>', methods=['GET'])
def get_user_info(username):
    """
    Query data related to username ans return as a json object
    """
    users = User.query.filter_by(username=username).all()  # it was supposed to be first
    return jsonify(user_json=[user.serialize for user in users])


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

        # username = request.query_string
        username = request.args.get('username')
        current_location_lat = float(request.args.get('location_lat'))
        current_location_long = float(request.args.get('location_long'))

        allsavedplaces = SavedPlaces.query.filter_by(username=username).all()

        # if allsavedplaces is not None:

        return jsonify(savedplaces_json=[savedplaces.serialize for allsavedplace in allsavedplaces])


# - End of points related to User Table
# ------------------------------------------------------
#   POST /create_save_place/ - create a new favorite place place in the database
@app.route('/create_save_place/', methods=['POST'])
def create_saveplace():
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

        querysavedplaces = current_session.query(SavedPlaces).filter_by(user_id=owner_id).all()

        if querysavedplaces is not None:
            # parsing previous locations to confirm if it is unique the new entry
            for location in querysavedplaces:

                distance_location, same_location = gf.verify_distance(float(locationlat), float(locationlong),
                                                                      float(location.location_lat),
                                                                      float(location.location_long), RADIUS_CIRCLE)
                # if the user is inserting a place already saved, previous location will be kept, and modified_stamp will be changed
                if same_location is True:
                    location.modified_timestamp = modified_timestamp
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
                    return "OK modified time update"  # exit function

        savedplaces = SavedPlaces(created_timestamp=created_timestamp, modified_timestamp=modified_timestamp,
                                  location_lat=locationlat, location_long=locationlong,
                                  address=address, waiting_time=waiting_time, user_id=owner_id)
        try:
            current_session.add(savedplaces)  # add opened statement to opened session
            current_session.commit()  # commit changes
        except:
            current_session.rollback()
            current_session.flush()  # for resetting non-commited .add()
        finally:
            current_session.close()

    return "new location inserted"


# ----------------------------------------------------------------------
# route to update the waiting time

@app.route('/update_saved_places/', methods=['POST'])
def updatesavedplaces():
    if not request.json or not 'location_lat' in request.json or not 'location_long' in request.json or not 'username' in request.json:
        abort(404)

    # parsing request data
    # -------------------------

    content = request.get_json(force=True)
    created_timestamp = datetime.datetime.now()
    modified_timestamp = datetime.datetime.now()  # get a new data to update
    username = content["username"]
    locationlat = content["location_lat"]
    locationlong = content["location_long"]
    waiting_time = content["waiting_time"]
    address = content["address"]
    # ---------------------------

    current_session = db.session  # open database session

    # query table USer to get username and then query by user
    owner_id = current_session.query(User).filter_by(username=username).first().username

    if owner_id is not None:

        # get all saved places by all users
        querysavedplaces = current_session.query(SavedPlaces).filter_by().all()

        if querysavedplaces is not None:

            # parsing query
            for location in querysavedplaces:
                # verify if the distance of the newlocation is already in the database, or if there is a close location
                # verifying that calculating distance of 2 points, it will be considered as same place if the distance btw 2 points is smaller than 10 m
                distance_location, same_location = gf.verify_distance(float(locationlat), float(locationlong),
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

    return "ok"


# --------------------------------------------------------------------------------------------------------
# Routes to Website

@app.route('/map/')
def get_map():
    return render_template('map.html')


@app.route('/debugger/')
def display_debug_message():
    """Display session and preserves dictionary format in bootbox alert."""

    return jsonify(session)


'''

# Delete saved place
@app.route('/delete_saved_place/', method = ['POST'])
def delete_saved_place():
    if not request.json or not 'location_lat' in request.json or not 'location_long' in request.json or not 'username' in request.json:
        abort(404)

    return "ok"


# catch page error
# ----------------------
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
# -----------------------------
'''
# ----------------------


#lat = request.args.get('lat')
#long = request.args.get('long')

if __name__ == '__main__':
    connect_to_db(app)

    app.run(debug=True)
