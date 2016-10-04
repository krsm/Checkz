from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim  # used to get address based on lat and longitude




def verify_distance(lat1,lon1, lat2, lon2, radius ):


    """

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    radius = max distance the one location could be from each other to be considered as equal
    radius in meters

    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    distance = (c*r)*1000  # distance in meters

    if distance <= radius:
        return distance, True
    else:
        return distance, False



def get_location_address(lat,long):

    """
    Return location address based on
    :param lat:
    :param long:
    :return:
    """
    place = str(lat)+","+str(long)

    print(place)


    geolocator = Nominatim()
    location = geolocator.reverse(place)

    return location.address

def compare_addresses(ad1,ad2):
    """


    :param ad1:
    :param ad2:
    :return:
    """
    # this function has to be improved

    if ad1 == ad2:
        return True
    else:
        return False





if __name__ == '__main__':

    durhamlat = 35.9940
    durhamlong =78.8986
    raleighlat =35.7796
    raleighlong = 78.6382

    # Raleigh 35.7796° N, 78.6382° W

    # Durham 35.9940° N, 78.8986° W

    print(verify_distance(durhamlat,durhamlong,raleighlat,raleighlong,5))
    print(get_location_address(78.8986,35.9940))