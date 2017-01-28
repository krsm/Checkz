# -*- coding: utf-8 -*-
import googlemaps
from googlemaps.distance_matrix import distance_matrix as dm
from .config import GOOGLE_API_KEY

from datetime import datetime
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

# # Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#
# #print(type(geocode_result))
#
# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((37.3860517, -122.0838511))
#
#
# print(reverse_geocode_result[0]['formatted_address'])

def formatted_address(lat, long):
    lat = float(lat)
    long = float(long)

    # Look up an address with reverse geocoding
    # reverse_geocode_result = gmaps.reverse_geocode((37.3860517, -122.0838511))

    reverse_geocode_result = gmaps.reverse_geocode((lat, long))

    return reverse_geocode_result[0]['formatted_address']


def get_duration_in_traffic(origins, destinations):

    now = datetime.now()
    matrix = dm(gmaps, origins, destinations,
                mode="driving",
                language="en-AU",
                avoid="tolls",
                units="imperial",
                departure_time=now,
                traffic_model="optimistic")

    return matrix['rows'][0]['elements'][0]['duration_in_traffic']['text']

#
# if __name__ == "__main__":
#
#     origins = ["Mebane, North Caolina"]
#     destinations = ["Morrisville, North Carolina"]
#
#     now = datetime.now()
#     matrix = dm(gmaps, origins, destinations,
#                 mode="driving",
#                 language="en-AU",
#                 avoid="tolls",
#                 units="imperial",
#                 departure_time=now,
#                 traffic_model="optimistic")
#     # print(formatted_address(37.3860517, -122.0838511))
#
#     print(matrix['rows'][0]['elements'][0]['duration_in_traffic']['text'])
