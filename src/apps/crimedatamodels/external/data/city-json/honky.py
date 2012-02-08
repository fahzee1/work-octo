#!/usr/bin/env python

import difflib
import glob
import itertools
import json
import math

class CandidateCity(object):
    def __init__(self, result_json, crimes_by_city):
        self.city_names = []
        self.neighborhood_names = []
        self.county_names = []
        self.zip_code = None
        self.state = None
        self.geometries = []
        self.geometry = result_json['geometry']['location']
        for component in result_json['address_components']:
            if 'locality' in component['types']:
                self.city_names.append(component['short_name'])
            if 'sublocality' in component['types']:
                self.neighborhood_names.append(component['short_name'])
            if 'administrative_area_level_3' in component['types']:
                self.neighborhood_names.append(component['short_name'])
            if 'administrative_area_level_2' in component['types']:
                self.county_names.append(component['short_name'])
            if 'administrative_area_level_1' in component['types']:
                self.state = component['short_name']
            if 'postal_code' in component['types']:
                self.zip_code = component['short_name']
        self.all_candidate_names = list(itertools.chain(
            self.city_names, self.neighborhood_names, self.county_names))
        self.exact = False
        self.best_name = None
        self.compute_best_match_city_name(crimes_by_city)
    def compute_best_match_city_name(self, crimes_by_city):
        best_names = difflib.get_close_matches(
            crimes_by_city.fbi_city_name, self.all_candidate_names)
        if best_names and best_names[0] == crimes_by_city.fbi_city_name:
            self.best_name = best_names[0]
            if self.state == crimes_by_city.state.abbreviation:
                self.exact = True
        #print "NAME", self.best_name, self.exact
    def __repr__(self):
        return "%s <%s>" % (self.city_names, self.geometry)
def json_to_candidate_cities(infile, crimes_by_city):
    candidate_cities = []
    with open(infile) as f:
        city_json = json.load(f)
    results = sorted(city_json['results'], reverse=True,
        key=lambda r: 'locality' in r['types'])
    for result in results:
        candidate_cities.append(CandidateCity(result, crimes_by_city))
    return candidate_cities

def deg2rad(degrees):
    return math.pi*degrees/180.0
def rad2deg(radians):
    return 180.0*radians/math.pi

# Semi-axes of WGS-84 geoidal reference
WGS84_a = 6378137.0  # Major semiaxis [m]
WGS84_b = 6356752.3  # Minor semiaxis [m]

# Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
def WGS84_earth_radius(lat):
    # http://en.wikipedia.org/wiki/Earth_radius
    An = WGS84_a*WGS84_a * math.cos(lat)
    Bn = WGS84_b*WGS84_b * math.sin(lat)
    Ad = WGS84_a * math.cos(lat)
    Bd = WGS84_b * math.sin(lat)
    return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

# Bounding box surrounding the point at given coordinates,
# assuming local approximation of Earth surface as a sphere
# of radius given by WGS84
def latlng_bounding_box(latitude, longitude, half_side):
    lat = deg2rad(latitude)
    lon = deg2rad(longitude)
    half_side_m = 1000*half_side # km to m

    # Radius of Earth at given latitude
    radius = WGS84_earth_radius(lat)
    # Radius of the parallel at given latitude
    pradius = radius*math.cos(lat)

    lat_min = lat - half_side_m/radius
    lat_max = lat + half_side_m/radius
    lon_min = lon - half_side_m/pradius
    lon_max = lon + half_side_m/pradius

    return (rad2deg(lat_min), rad2deg(lon_min),
            rad2deg(lat_max), rad2deg(lon_max))

def main():
    files = glob.glob('**/*.json')
    #files = ['savannah-chatham-metropolitan-georgia.json']
    crimes_by_city = lambda: None
    crimes_by_city.fbi_city_name = 'Savannah'
    crimes_by_city.state = lambda: None
    crimes_by_city.state.abbreviation = 'GA'
    for file in files:
        city = json_to_candidate_cities(file, crimes_by_city)
        if not city:
            print "NO CITIES %s %s" % (file, city)
        if len(city) > 1:
            print "MULTIPLE CANDIDATES %s %s" % (file, city)
        elif len(city[0].city_names) > 1:
            print "MULTIPLE LOCALITY: %s" % (file), city[0].best_name, city[0].exact
        elif not city[0].city_names:
            print "EMPTY LOCALITY %s" % (file), city[0].best_name, city[0].exact


def geo_distance(lat1, lng1, lat2, lng2):
    (lat1, lng1) = (deg2rad(lat1), deg2rad(lng1))
    (lat2, lng2) = (deg2rad(lat2), deg2rad(lng2))
    delta_lat = lat1 - lat2
    delta_lng = lng1 - lng2
    radius = WGS84_earth_radius(lat1)
    return radius*2*math.asin(
        math.sqrt(
            math.sin(delta_lat/2.0) ** 2 +
            math.cos(lat1)*math.cos(lat2)*(math.sin(delta_lng/2.0)**2)))
    return 0

if __name__ == '__main__':
    main()
## SELECT * FROM `crime_data`.`zip_codes`
## WHERE (latitude BETWEEN 39.0 AND 39.9) AND
## (`longitude` BETWEEN -83.9 AND -83.0)
## AND city != ''
## ORDER BY `city`
