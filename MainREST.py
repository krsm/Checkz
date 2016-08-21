# Import settings.
from flask import Flask,request, jsonify,g,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import strftime, gmtime
import os

#------------------------------------------------

PATH_DB = 'sqlite:////home/km/Dropbox/Git_Local/00 - Python/FlaskRestAlchemy/UserLocationApi'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = PATH_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']= os.urandom(24)# will be used in the cookie - to encrypt the cookie

db = SQLAlchemy(app)

# database colums
#Id, timestamp, location_lat, location_long
#    timestamp BLOB,
#    location_lat NUMERIC,
#    location_long NUMERIC)
#                          ''')
class UserData(db.Model):
    __tablename__ = 'UserData'
    id = db.Column('ID',db.Integer,primary_key=True)
    timestamp = db.Column('timestamp',db.Unicode)
    location_lat = db.Column('location_lat',db.String(100))
    location_long = db.Column('location_long',db.String(100))


    def __init__(self,id,timestamp,locaiton_lat, location_long):
        self.id = id
        self.timestamp = timestamp
        self.location_lat = locaiton_lat
        self.location_long = location_long



# Inserting data
# Using Method Post
#-------------------------------------------

@app.route('/checkz/post/',methods=['POST'])
#def insertdatatable(db,timestamp,location_lat,location_long):
def postlocation():

    #date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    if not request.json or not 'location_lat' in request.json or not 'location_long' in request.json:
        abort(404)

    content = request.get_json(force=True)
    #content = json.dumps(content)
    #timestamp=content["timestamp"]
    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    location_lat = content["location_lat"]
    location_long = content["location_long"]
    datafiles=[timestamp,location_lat,location_long]

    #create object to insert in the database
    #prepare query statement
    userdata = UserData(timestamp=timestamp,location_lat=location_lat,location_long=location_long)
    currentsesstion = db.session#open database seesion

    try:
        currentsesstion.add(userdata) # add opened statement to opened session
        currentsesstion.commit()#commit changes
    except:
        currentsesstion.rollback()
        currentsesstion.flush()#for resetting non-commited .add()


    return None




@app.route('/checkz/get/', methods=['GET'])
def getlocation():

    all_location = UserData.query.all() # fetch all entries on the table
    lat =[]
    long = []

    for location in all_location:
        lat.append(location.location_lat)

    for location in all_location:
        long.append(location.location_long)

    cur = [
        {
        'latitude':lat[0]
        },
        {
        'longitude':long[0]
        }
    ]


    return jsonify({"location_json":cur})

"""
        self.id = id
        self.timestamp = timestamp
        self.location_lat = locaiton_lat
        self.location_long = location_long

"""

#catch page error
#----------------------
@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

#-----------------------------

#@app.before_request to run a function before every request from the browser:
@app.before_request
def before_request():
    db.session()

#@app.teardown_request to close the database connection after every request.
@app.teardown_request
def teardown_request(exception):
    db.session.remove()

if __name__ == '__main__':
    #print(globals())
    app.run(debug=True)



