import requests

url_post = 'http://127.0.0.1:5000/get_user/'

data = {'username': 'km'}

r = requests.get(url_post, data)
print(r.url)
print(r.status_code)

"""


curl -i -H "Content-Type: application/json" -X POST -d '{"username":"sdfsdfsd"}' http://127.0.0.1:5000/create_user/

curl -i -H "Content-Type: application/json" -X GET -d http://127.0.0.1:5000/get_user/km

curl -i -H "Content-Type: application/json" -X GET -d http://127.0.0.1:5000/get_all_saved_places/?username=finaluser&latitude=12&longitude=12


http://127.0.0.1:5000/

curl -i -H "Content-Type: application/json" -X POST -d '{"username":"finaluser","location_lat":"0.1","location_long":"0.1","waiting_time":"0","address":"0"}' http://127.0.0.1:5000/create_save_place/

curl -i -H "Content-Type: application/json" -X POST -d '{"username":"finaluser","location_lat":"0.1","location_long":"0.1","waiting_time":"10","address":"0"}' http://127.0.0.1:5000/update_saved_places/



  events = Events.query.filter_by(event_type = event_type).all()
return jsonify(json_list = [event.serialize for event in events])
"""


#curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/get_saver_places/locationdata?latitude=33.0&&longitude=33.0&&address=rua+sao+januario