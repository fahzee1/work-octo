"""
Associate CrimesByCity instances to CityLocation instances by prompting a human
"""
from collections import namedtuple, deque
import decimal
import json
import math
from optparse import make_option
import os
import re
import rlcompleter # to jazz up readline
import readline # to jazz up raw_input
from string import capwords
import sys

from django.core.management.base import BaseCommand, CommandError

from apps.crimedatamodels.models import CrimesByCity, ZipCode, CityLocation

class Nub(object):
    """A dummy object to be used like a dynamic C-struct"""
    def __init__(self, **kwargs):
        """Accepts keyword args as optional initial attributes"""
        self.__initial_attrs = {}
        for (key, val) in kwargs.iteritems():
            self.__initial_attrs[key] = val
            setattr(self, key, val)
    def __repr__(self):
        result = "Nub(%s)" % (self.__initial_attrs)
        return result

class Command(BaseCommand):
    help = "Associate CrimesByCity instances with CityLocation instances by prompting a human"
    option_list = BaseCommand.option_list + (
        make_option('-J', '--json-dir', dest='json_dir',
            help='Data directory where Google Maps json files can be '+
            'found. Google Maps json files should be named as '+
            'state/city.json where `state` is a state abbreviation. '+
            'For example, tx/round-rock.json. '),
        make_option('-V', '--verbose', action='store_true', default=False,
            dest='verbose', help='talk about everything that happens'),
    )

    def handle(self, *args, **options):
        if options['json_dir'] is not None:
            app = lambda: None # dummy object
            app.options = options

            lost_cities = CrimesByCity.objects.extra(where=['NOT EXISTS (SELECT * FROM citylocations WHERE citylocations.city_name = crimes_by_city.fbi_city_name AND citylocations.state = crimes_by_city.fbi_state)']).values('fbi_city_name','fbi_state').distinct()
            lost_cities = [Nub(**city) for city in lost_cities]

            for city in lost_cities:
                if options['verbose']:
                    print "Processing %s, %s" % (
                        city.fbi_city_name,
                        city.fbi_state)
                attach_alternate_city_names(city)
                attach_json_paths(city)

                # dump "(and Other City)" from fbi_city_name
                crimes_by_city = city
                city_name = crimes_by_city.fbi_city_name
                city_name = re.sub(r' ?\([^\)]*\)', '', city_name)
                fbi_city_names = [city_name]
                fbi_city_names.extend(crimes_by_city.alternate_city_names)
                crimes_by_city.fbi_city_names = fbi_city_names
                crimes_by_city.google = {}
                for candidate_fbi_city_name in fbi_city_names:
                    load_google_data(app, crimes_by_city, candidate_fbi_city_name)
                assemble_and_prompt(crimes_by_city)
        else:
            raise CommandError("Missing args. See --help")
def assemble_and_prompt(city):
    """Create CandidateLocations for each GoogleData Result and prompt for
    human confirmation"""
    candidates = []
    for city_name in city.fbi_city_names:
        google_data = city.google[city_name]
        if google_data is None:
            continue
        for result in google_data.results:
            candidates.append(
                Nub(
                    city=list(result.city.union(result.alternate)),
                    state=result.state,
                    latitude=result.latitude, longitude=result.longitude))
    # basic info
    print "# %-50s %2s" % (city.fbi_city_name, city.fbi_state)
    # candidate info before prompt
    for (index, candidate) in enumerate(candidates):
        print "%d %-50s %2s %010.6f,%010.6f" % (
            index, candidate.city, candidate.state, candidate.latitude, candidate.longitude)
    # prompt options
    print "----"
    print "Enter # or custom lat,lng"
    answer = get_valid_response(len(candidates))
    if isinstance(answer, int):
        location = CityLocation(city_name=city.fbi_city_name,
            state=city.fbi_state,
            latitude=candidates[answer].latitude,
            longitude=candidates[answer].longitude)
    else:
        (lat,lng) = answer.split(',')
        (lat,lng) = (float(lat), float(lng))
        location = CityLocation(city_name=city.fbi_city_name,
            state=city.fbi_state,
            latitude=lat,longitude=lng)
    print "Saving %s, %s %010.6f,%010.6f\n" % (
        location.city_name, location.state, location.latitude,
        location.longitude)
    location.latitude = decimal.Decimal("%010.6f" % location.latitude)
    location.longitude = decimal.Decimal("%010.6f" % location.longitude)
    location.save()
def get_valid_response(candidate_count):
    while True:
        intext = raw_input("--> ")
        if re.search(r',', intext):
            (lat,lng) = intext.split(',')
            try:
                (lat, lng) = (float(lat), float(lng))
            except ValueError:
                continue
            else:
                return intext
        else:
            try:
                choice = int(intext)
            except ValueError:
                continue
            else:
                if 0 <= choice < candidate_count:
                    return choice
            
def load_google_data(app, city, city_name):
    jsonpath = os.path.join(app.options['json_dir'],
        city.json_paths[city_name])
    if not os.path.exists(jsonpath):
        print >>sys.stderr, "Missing json file; run google?"+\
            " %s %s (%s)" % (city.fbi_city_name, city.fbi_state, city_name)
        city.google[city_name] = None
        return
    with open(jsonpath) as f:
        json_results = json.load(f)
    google_data = GoogleData(city, city_name, json_results)
    city.google[city_name] = google_data
def massage_place_name(name):
    name = re.sub(r'(\d),', r'\1', name) # strip commas from long numbers
    name = re.sub(r'(\w),(\w)', r'\1, \2', name)
    name = re.sub(r'(\D)\d+', r'\1', name) # trailing footnote no. Illinois6
    name = re.sub(r'^\s+|\s$', r'', name) # name.strip()
    name = re.sub(r'[ ]{2,}', ' ', name) # strip double+ spaces
    name = capwords(name)
    name = re.sub(r'\bOf\b', 'of', name)
    return name
def attach_alternate_city_names(city):
    """Alternate city names for 'Village', 'Township', 'Town', etc."""
    city.alternate_city_names = generate_alternate_city_names(
        city.fbi_city_name)
def generate_alternate_city_names(city_name):
    alternate_city_names = []
    # drop ", NameOfCounty" and "(and CoReportedTown)"
    patterns = (r'[ ]*[,].*', r'[ ]*\([^\)]*\)')
    for pattern in patterns:
        pattern = re.compile(pattern, re.IGNORECASE)
        if re.search(pattern, city_name):
            city_name = re.sub(pattern, '', city_name)
            alternate_city_names.append(city_name)
    # split McTownName into Mc TownName
    patterns = (r'\bMc(\w+)',)
    for pattern in patterns:
        pattern = re.compile(pattern, re.IGNORECASE)
        if re.search(pattern, city_name):
            newname = re.sub(pattern, r'Mc \1', city_name)
            alternate_city_names.append(newname)
    patterns = (r'\bvillage\b', r'\btownship\b', r'\btown\b', r'\bregional\b',
        r'\bcity\b')
    for pattern in patterns:
        pattern = re.compile(pattern, re.IGNORECASE)
        if re.search(pattern, city_name):
            newname = re.sub(pattern, '', city_name)
            pattern = re.compile(r'\bSt(\.|\b)', re.IGNORECASE)
            newname = re.sub(pattern, 'Saint', newname)
            newname = re.sub(r'^\s+|\s+$', '', newname)
            alternate_city_names.append(newname)
    pattern = re.compile(r'\bSt(\.|\b)', re.IGNORECASE)
    if re.search(pattern, city_name):
        newname = re.sub(pattern, 'Saint', city_name)
        newname = re.sub(r'^\s+|\s+$', '', newname)
        alternate_city_names.append(newname)
    pattern = re.compile(r'\bMount\b', re.IGNORECASE)
    if re.search(pattern, city_name):
        newname = re.sub(pattern, 'Mt', city_name)
        newname = re.sub(r'^\s+|\s+$', '', newname)
        alternate_city_names.append(newname)
    alternate_city_names = map(massage_place_name, alternate_city_names)
    return alternate_city_names
def attach_json_paths(city):
    """Create json paths for each potential city name"""
    city.json_paths = {}
    city_names = [city.fbi_city_name]
    city_names.extend(city.alternate_city_names)
    for city_name in city_names:
        city.json_paths[city_name] = get_json_path(
            city.fbi_state, city_name)
def get_json_path(state, city_name):
    """Generate a filename with characters that won't bork filesystems"""
    city_name = city_name.lower()
    city_name = re.sub(r"[']+", '', city_name)
    city_name = re.sub(r'[? ,/._()-]+', '-', city_name)
    city_name = re.sub(r'^-+|-+$', r'', city_name)
    city_name = ''.join([city_name, '.json'])
    state = state.lower()
    return os.path.join(state, city_name)
def deg2rad(degrees):
    return math.pi*float(degrees)/180.0
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
    return math.sqrt((An*An + Bn*Bn)/(Ad*Ad + Bd*Bd))
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

    return (
        decimal.Decimal("%010.6f" % rad2deg(lat_min)),
        decimal.Decimal("%010.6f" % rad2deg(lon_min)),
        decimal.Decimal("%010.6f" % rad2deg(lat_max)),
        decimal.Decimal("%010.6f" % rad2deg(lon_max)))
def geo_distance(lat1, lng1, lat2, lng2):
    (lat1, lng1) = (deg2rad(lat1), deg2rad(lng1))
    (lat2, lng2) = (deg2rad(lat2), deg2rad(lng2))
    delta_lat = lat1 - lat2
    delta_lng = lng1 - lng2
    radius = WGS84_earth_radius(lat1)
    return decimal.Decimal("%010.6f" % (radius*2*math.asin(
        math.sqrt(
            math.sin(delta_lat/2.0) ** 2 +
            math.cos(lat1)*math.cos(lat2)*(math.sin(delta_lng/2.0)**2)))))

class GoogleData(object):
    """Google's response for a city. A Google response may have 0 or more
    results."""
    Result = namedtuple('Result',
        'city state latitude longitude zip alternate')
    def __init__(self, crimes_by_city, city_name, city_json):
        self.states = set()
        self.city_names = set()
        self.alternate_names = set()
        self.zips = set()
        self.results = deque()
        for result in city_json.get('results', []):
            lat = result['geometry']['location']['lat']
            lng = result['geometry']['location']['lng']
            (city, alternate, state, zip) = (set(), set(), None, None)
            for component in result['address_components']:
                if 'locality' in component['types']:
                    city.add(massage_place_name(component['short_name']))
                if 'sublocality' in component['types']:
                    alternate.add(massage_place_name(component['short_name']))
                if 'administrative_area_level_3' in component['types']:
                    alternate.add(massage_place_name(component['short_name']))
                if 'administrative_area_level_2' in component['types']:
                    alternate.add(massage_place_name(component['short_name']))
                if 'administrative_area_level_1' in component['types']:
                    state = component['short_name']
                if 'postal_code' in component['types']:
                    zip = component['short_name']
            self.results.append(
                GoogleData.Result(city, state, lat, lng, zip, alternate))
            if city:
                self.city_names.update(city)
            if alternate:
                self.alternate_names.update(city)
            if state:
                self.states.add(state)
            if zip:
                self.zips.add(zip)
        self.fix_broken_states(crimes_by_city, city_name)
    def fix_broken_states(self, crimes_by_city, city_name):
        for (index, result) in enumerate(self.results):
            if result.state is None:
                # If Google's result is within 16km (about 10 miles) of
                # a zip code in the right state, then consider it in the state
                nearest_zips = nearest_zips_to_latlng(
                    result.latitude, result.longitude)
                if nearest_zips is not None:
                    nearest_zip_states = set([z.state for z in nearest_zips])
                    if crimes_by_city.fbi_state in nearest_zip_states:
                        self.results[index] = result._replace(
                            state=crimes_by_city.fbi_state)
                        self.states.add(crimes_by_city.fbi_state)
def nearest_zips_to_latlng(latitude, longitude):
    """Retrieve up to 10 known zip-codes within 16km (~10mi) of the given
    location, sorted nearest first"""
    (lat_min, lng_min, lat_max, lng_max) = latlng_bounding_box(
        latitude, longitude, 16.0)
    candidate_zips = list(ZipCode.objects.filter(
        latitude__gte=lat_min,
        latitude__lte=lat_max,
        longitude__gte=lng_min,
        longitude__lte=lng_max).exclude(city=''))
    candidate_zips.sort(key=lambda zip: geo_distance(
        latitude, longitude, zip.latitude, zip.longitude))
    return candidate_zips
def flatten(xs):
    return [item for sublist in xs for item in sublist]
