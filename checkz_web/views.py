# -*- coding: utf-8 -*-
import datetime
from functools import wraps

from flask import Flask, render_template, redirect, request, session, jsonify
from flask import url_for

import checkz_web.geofuntcions as gf
import checkz_web.maps as maps
# from checkz_web import db
from checkz_data.database import db_session
from checkz_data.models import User, SavedPlaces

from . import app

from checkz_web.constants import RADIUS_CIRCLE, RADIUS_SAVED_PLACES, type_of_locations, median_waiting_time

# ------------------------------------------------
# Create a flask app and set a random secret key
# Create the app
# app = Flask("Checkz"
#             # instance_path=get_instance_folder_path(),
#             # instance_relative_config=True,
# #             # template_folder='templates'
#             )
# applying config
# configure_app(app)
# db.init_app(app)

# app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# TODO move to a config/setup file togetther with all constants
# app.secret_key = os.urandom(32)

# raises error if you use an undefined variable in Jinja2
# app.jinja_env.undefined = StrictUndefined


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# login required decorator
# TODO verify username in the session
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated

# Application Routes
# ------------------
# ================================================================================
#  Registration, Login, and User Profile
# ================================================================================
# @app.before_request
# def before_request():
#     g.user = None
#     if 'username' in session:
#         g.user = session['username']

@app.route('/register', methods=['POST', 'GET'])
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
            #
            # db_session = db_session  # open database session

            try:
                db_session.add(user)  # add opened statement to opened session
                db_session.commit()  # commit changes

                # initiate the session with the current user
                # create a user_id session
                session['user_id'] = user.id
                session['username'] = pending_user

            except:
                db_session.rollback()
                db_session.flush()  # for resetting non-commited .add()

                # In case of fail not start the session with
                session['user_id'] = None
                session['username'] = None

                # finally:
                #     db_session.close()

        return redirect(url_for("home_page"))

    else:
        # error = "405  Method not allowed"
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    # db_session = db_session  # open database session
    error = None
    if request.method == 'POST':

        password = request.form['password']
        email = request.form['email']

        possible_user = User.query.filter_by(email=email).first()

        if possible_user and possible_user.verify_password(password):

            session['username'] = possible_user.username
            session['user_id'] = possible_user.id
            db_session.close()
            return redirect(url_for("home_page"))

        else:
            error = "Invalid Credentials. Please try again."
            db_session.close()
            return render_template("login.html", error=error)

    else:
        # error = "405  Method not allowed"
        db_session.close()
        return render_template("login.html", error=error)


# TODO confirm need to decorate function with login required
@app.route('/logout/')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    # session['user_id'] = None
    # session['username'] = None
    # this remove the entire session dictionary
    session.clear()
    # to avoid to show logout in the url_browser
    return redirect(url_for("home_page"))


# Homepage
@app.route('/')
def home_page():
    return render_template("map.html")


# # render_map route
# It is called when the logo is pressed
@app.route('/render_map')
def render_map():
    return render_template("map.html")


# Code related to show details page
@app.route('/show_details', methods=['GET'])
def render_show_details():
    return render_template("show_details.html")


# Code related to about page
@app.route('/about_page')
def about_page():
    return render_template("about.html")

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
    user_id = request.args.get('user_id')

    # if user_id is not None:

    # db_session = db_session  # open database session

    # query all previous saved places for certain user

    # allsavedplaces = db_session.query(SavedPlaces).filter_by(user_id=user_id).all()

    allsavedplaces = SavedPlaces.query.filter_by(user_id=user_id).all()

    # TODO evaluate use the user current location to display just the saved places in a range closer to user current location

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

    db_session.close()

    return jsonify({"saved_places": saved_places})

    # TODO use @property method of class to serialize response
    # return jsonify(savedplaces_json=[SavedPlaces.serialize for allsavedplace in allsavedplaces])


# - End of points related to User Table
# ------------------------------------------------------
#   POST /create_save_place/ - create a new favorite place place in the database
@app.route('/save_favorite_place/', methods=['POST', 'GET'])
def save_favorite_place():
    """ Save user's favorite spot to db """
    # parsing request data
    # -------------------------
    created_timestamp = datetime.datetime.now()
    modified_timestamp = datetime.datetime.now()
    user_id = request.form["user_id"]
    location_lat = float(request.form["location_lat"])
    location_long = float(request.form["location_long"])
    type_location = request.form["type_location"]

    # TODO verify address with another geocode address
    # to be improved and use google geocoding
    address = maps.formatted_address(location_lat, location_long)
    # variable to be returned as json
    saved_places = []

    # First interaction using all data related to the same user

    # type_of_locations is a global variable what contains possible types of places
    if type_location in type_of_locations:

        # in case of average waiting time will be used, based on the kind of place
        waiting_time = median_waiting_time[type_location]

        # db_session = db_session  # open database session
        # username = db_session.query(User).filter_by(id=user_id).first().username

        # query by all previous saved places of a certain user

        current_user_places = db_session.query(SavedPlaces).filter_by(user_id=user_id).all()
        #
        if current_user_places is not None:

            for user_places in current_user_places:

                # print(user_places.address)

                # distance_location, same_location = gf.verify_distance(location_lat, location_long,
                #                                                       float(user_places.location_lat),
                #                                                       float(user_places.location_long), RADIUS_CIRCLE)

                # if location is the same as previous saved one,
                # it will be considered as an updated for
                # a certain location
                if address == user_places.address:
                    # updating modified_timestamp
                    user_places.modified_timestamp = datetime.datetime.utcnow()
                    # update type_location
                    user_places.type_location = type_location

                    try:
                        # db_session.add(user_places)  # add opened statement to opened session
                        db_session.commit()  # commit changes
                    except Exception as e:
                        db_session.rollback()
                        db_session.flush()  # for resetting non-commited .add()

                    # in this case user was saving/updating a previous saved location
                    saved_places.append({'favorite_updated': "ok"})
                    return jsonify({"saved_places": saved_places})

        # # query all users previous saved places
        # all_users_places = db_session.query(SavedPlaces).all()
        #
        # # saving a favorite place for the first time
        # # to avoid to loop trough a empty object
        # if all_users_places is not None:
        #     for previous in all_users_places:
        #
        #         distance_location, same_location = gf.verify_distance(float(location_lat), float(location_long),
        #                                                               float(previous.location_lat),
        #                                                               float(previous.location_long), RADIUS_CIRCLE)
        #         # # lat and long are inside a certain RADIUS_CIRCLE
        # if same_location is True or address is previous.address:
        #     waiting_time = previous.waiting_time
        #     # in case of address is equal and lat and long are different
        #     # break

        # creating a new place to database
        new_favorite = SavedPlaces(created_timestamp=created_timestamp, modified_timestamp=modified_timestamp,
                                   location_lat=location_lat, location_long=location_long,
                                   address=address, waiting_time=waiting_time, type_location=type_location,
                                   user_id=user_id)
        try:
            db_session.add(new_favorite)  # add opened statement to opened session
            db_session.commit()  # commit changes
        except Exception as e:
            db_session.rollback()
            db_session.flush()  # for resetting non-commited .add()

        saved_places.append({'favorite_created': "ok"})
        return jsonify({"saved_places": saved_places})

    # case in what type_location was not defined
    else:
        return jsonify({"saved_places": saved_places})


# function to verify if a certain location is already in the database
def is_location_on_database():

    location_db = True

    return location_db


# route to remove favorite place
@app.route('/remove_favorite_place', methods=['POST'])
def remove_favorite_place():
    """ Remove user's favorite spot to db """

    user_id = request.form.get('user_id')
    location_lat = request.form.get("location_lat")
    location_long = request.form.get("location_long")

    # db_session = db_session  # open database session

    # to_be_removed = db_session.query(SavedPlaces).filter_by(SavedPlaces.user_id == user_id, SavedPlaces.location_lat ==location_lat,
    #                                                         SavedPlaces.location_long == location_long).first()
    to_be_removed = SavedPlaces.query.filter(SavedPlaces.user_id == user_id, SavedPlaces.location_lat == location_lat,
                                             SavedPlaces.location_long == location_long).delete()
    if to_be_removed is not None:

        try:
            SavedPlaces.query.filter(SavedPlaces.user_id == user_id, SavedPlaces.location_lat == location_lat,
                                     SavedPlaces.location_long == location_long).delete()
            db_session.commit()
        except:
            db_session.rollback()
            db_session.flush()  # for resetting non-commited .add()
            # finally:
            #     db_session.close()

    return "Executed"
    # TODO finish query to see the lat and long and remove place from database


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
    # db_session = db_session  # open database session

    # query table USer to get username and then query by user
    owner_name = db_session.query(User).filter_by(id=user_id).first().username

    if owner_name is not None:

        # get all saved places by all users
        # querysavedplaces = db_session.query(SavedPlaces).filter_by().all()

        # to_be_removed = SavedPlaces.query.filter(SavedPlaces.user_id == user_id, SavedPlaces.location_lat == location_lat,
        #                                SavedPlaces.location_long == location_long).delete()

        allsavedplaces = SavedPlaces.query.filter(SavedPlaces.user_id == user_id,
                                                  SavedPlaces.location_lat == location_lat,
                                                  SavedPlaces.location_long == location_long).all()
        # print(allsavedplaces)

        # TODO evaluate use the user current location to display just the saved places in a range closer to user current location

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

        db_session.close()

        return jsonify({"saved_places": saved_places})


# route to update the waiting time
@app.route('/update_waiting_time', methods=['POST', 'GET'])
def update_waiting_time():
    # parsing request data
    # -------------------------

    user_id = request.form.get('user_id')
    location_lat = float(request.form.get('location_lat'))
    location_long = float(request.form.get('location_long'))
    waiting_time = request.form.get('updated_waiting_time')

    # print(waiting_time)

    created_timestamp = datetime.datetime.now()
    modified_timestamp = datetime.datetime.now()  # get a new data to update

    # ---------------------------
    # db_session = db_session  # open database session

    # query table USer to get username and then query by user
    owner_name = db_session.query(User).filter_by(id=user_id).first().username

    # db_session.close()
    #
    # db_session = db_session  # open database session
    #
    # current_user_place = db_session.query(SavedPlaces).filter(SavedPlaces.location_lat == location_lat,
    #                                                                SavedPlaces.location_long == location_long,
    #                                                                SavedPlaces.user_id == user_id).first()

    current_user_place = SavedPlaces.query.filter_by(location_lat=location_lat,
                                                     location_long=location_long,
                                                     user_id=user_id).first()

    print(current_user_place.address)

    if owner_name is not None:

        # get all saved places by all users
        querysavedplaces = db_session.query(SavedPlaces).filter_by().all()

        if querysavedplaces is not None:

            # parsing query
            for location in querysavedplaces:
                # verify if the distance of the new location is already in the database, or if there is a close location
                # verifying that calculating distance of 2 points, it will be considered as same place if the distance btw 2 points is smaller than 10 m
                distance_location, same_location = gf.verify_distance(location_lat, location_long,
                                                                      float(location.location_lat),
                                                                      float(location.location_long), RADIUS_CIRCLE)

                if same_location is True or location.address is current_user_place.address:
                    location.modified_timestamp = modified_timestamp
                    location.waiting_time = waiting_time

            try:
                db_session.add(location)
                db_session.commit()  # commit changes
            except:
                db_session.rollback()
                db_session.flush()  # for resetting non-commited .add()
                # finally:
                #     db_session.close()

    return "update_waiting_time_done"


# route to return info about places to user
# before user be logged in, display info related to places save by others
@app.route('/get_info_about_close_locations', methods=['GET'])
def get_info_about_close_locations():
    location_lat = request.args.get('location_lat')
    location_long = request.args.get('location_long')

    saved_places = []

    # db_session = db_session  # open database session

    # get all saved places by all users
    # TODO get the most update waiting time, use time_stamp to query
    # querysavedplaces = db_session.query(SavedPlaces).filter_by().all()
    querysavedplaces = db_session.query(SavedPlaces).order_by(SavedPlaces.modified_timestamp.desc()).all()

    # parsing query
    for location in querysavedplaces:
        # verify if the distance of the new location is already in the database, or if there is a close location
        # verifying that calculating distance of 2 points, it will be considered as close place if the distance btw 2 points is smaller than 15 miles
        distance_location, close_location = gf.verify_distance(float(location_lat), float(location_long),
                                                               float(location.location_lat),
                                                               float(location.location_long), RADIUS_SAVED_PLACES)
        # distance_location in meters
        # dispplay info related to 10 locations max
        if close_location is True and (len(saved_places) <= 5):
            # TODO different users can save the same location as diffrerent type
            # Create logic to verify if it is the same as place, and just append
            # if the place does not exist already in the list,
            # The waiting time is already the same...
            saved_places.append({'user_id': location.user_id,
                                 'created_timestamp': location.created_timestamp,
                                 'modified_timestamp': location.modified_timestamp,
                                 'location_lat': location.location_lat,
                                 'location_long': location.location_long,
                                 'address': location.address,
                                 'waiting_time': location.waiting_time,
                                 'type_location': location.type_location})
    db_session.close()

    return jsonify({"saved_places": saved_places})


@app.route('/get_direction_shortest_time', methods=['GET'])
def get_direction_shortest_time():
    # parsing request data
    # -------------------------
    user_id = request.args.get('user_id')
    location_lat = request.args.get('location_lat')
    location_long = request.args.get('location_long')
    waiting_time = request.args.get('updated_waiting_time')
    type_location = str(request.args.get('type_location'))

    # TODO insert error treatment for address
    current_address = maps.formatted_address(location_lat, location_long)

    # print(current_address)

    # TODO change the possible tyoe of location as a global variable
    # possible_locations = TYPE_OF_LOCATIONS

    saved_places = []

    # type_of_locations is a global variable what contains possible types of places

    if type_location in type_of_locations:

        # db_session = db_session  # open database session
        # query table USer to get username and then query by user
        owner_name = db_session.query(User).filter_by(id=user_id).first().username

        # print(owner_name)

        if owner_name is not None:

            # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
            # TODO evaluate all queries using session
            # querysavedplaces = SavedPlaces.query.filter_by(user_id=user_id, type_location=type_location).all

            # querysavedplaces = db_session.query(SavedPlaces).filter_by(user_id=owner_name).all()

            querysavedplaces = db_session.query(SavedPlaces).filter_by(user_id=user_id).all()

            traffic_time = {}
            aux_dic_traffic_time = {}

            for location in querysavedplaces:

                # print(location.id)
                # FIXME improve query to remove this if statement
                if location.type_location == type_location:

                    duration_time_traffic = maps.get_duration_in_traffic(current_address, location.address)

                    duration_time_traffic = float(duration_time_traffic.split()[0])

                    if location.waiting_time is not None:
                        waiting_time = float(location.waiting_time)

                        total_time = duration_time_traffic + waiting_time

                        traffic_time[location.id] = total_time

                        aux_dic_traffic_time[location.id] = [location.location_lat, location.location_long]

                        # TODO improve this function - maybe use new dict functionality
                        min_traffic_time = min(traffic_time, key=lambda x: traffic_time.get(x))

            saved_places.append({'location_lat': aux_dic_traffic_time[min_traffic_time][0],
                                 'location_long': aux_dic_traffic_time[min_traffic_time][1],
                                 'current_location_lat': location_lat,
                                 'current_location_long': location_long})
        db_session.close()
    else:
        pass
    # TODO verify else
    return jsonify({"saved_places": saved_places})


# TODO parse json response to get address
@app.route('/get_formatted_address', methods=['GET'])
def formatted_address():
    # parsing request data
    # -------------------------
    user_id = request.args.get('user_id')
    location_lat = request.args.get('location_lat')
    location_long = request.args.get('location_long')

    # db_session = db_session  # open database session
    # query table USer to get username and then query by user
    owner_name = db_session.query(User).filter_by(id=user_id).first().username

    if owner_name is not None:
        address = []

        address.append({'address': maps.formatted_address(location_lat, location_long)})

        return jsonify({"formatted_address": formatted_address})


# ============================================================
# Errors Handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# if __name__ == '__main__':
#     connect_to_db(app)
#
#     app.debug = True
#     # pdb.set_trace()
#     # Use the DebugToolbar
#     # DebugToolbarExtension(app)
#     #
#     # app.run(host="192.168.1.110")
#     app.run()
#     #
#     # update_wait_time_db()
