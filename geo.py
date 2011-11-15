# -*- coding: UTF-8 -*-
import math

SCALE = 222089.472

def get_distance_from_latlng(lat1, lng1, lat2, lng2):
    '''calculate distance(meter) from two geo point
    
    www.johndcook.com/python_longitude_latitude.html
    
    '''

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
    # mod by snow: changed to meters from km
    meter_coefficients = 6373000

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = lng1*degrees_to_radians
    theta2 = lng2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    #
    # mod by snow:
    # result in meters
    return round(arc * meter_coefficients, 3)

def get_lat_offset_by_distance(distance):
    '''calculate latitude offset by given distance(meter)'''
    return round(distance / SCALE, 7)

def get_lng_offset_by_distance(distance, lat):
    '''calculate longitude offset by given distance(meter) and latitude'''
    return round(distance / (math.cos(math.radians(lat)) * SCALE), 7)