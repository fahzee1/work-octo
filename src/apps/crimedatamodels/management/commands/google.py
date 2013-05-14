"""
Query Google Maps API for all potential city names for each CrimesByCity
instance
"""
from datetime import datetime, timedelta
import json
from optparse import make_option
import os
import Queue
import re
import threading
import time
import urllib, urllib2

from django.core.management.base import BaseCommand, CommandError

from apps.crimedatamodels.models import CrimesByCity

class Command(BaseCommand):
    help = "Google any city names or alternate city names not yet googled"
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
            app.google_daemon = GoogleMapsQueryDaemon(app, delay=35)
            app.fbi_daemon = FBIDaemon(app)
            for daemon in (app.google_daemon, app.fbi_daemon):
                daemon.start()

            for city in CrimesByCity.objects.all().values(
                'fbi_city_name','fbi_state').distinct():
                crimes_by_city = lambda: None # dummy object
                crimes_by_city.fbi_city_name = city['fbi_city_name']
                crimes_by_city.fbi_state = city['fbi_state']
                if options['verbose']:
                    print "Processing %s, %s" % (
                        crimes_by_city.fbi_city_name,
                        crimes_by_city.fbi_state)
                attach_alternate_city_names(crimes_by_city)
                attach_json_paths(crimes_by_city)
                app.fbi_daemon.put(crimes_by_city)
            app.fbi_daemon.put(None, priority=200)
        else:
            raise CommandError("Missing args. See --help")
def attach_alternate_city_names(crimes_by_city):
    """Alternate city names for 'Village', 'Township', 'Town', etc."""
    crimes_by_city.alternate_city_names = generate_alternate_city_names(
        crimes_by_city.fbi_city_name)
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
            city_name = re.sub(pattern, r'Mc \1', city_name)
            alternate_city_names.append(city_name)
    patterns = (r'\bvillage\b', r'\btownship\b', r'\btown\b', r'\bregional\b')
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
    return alternate_city_names
def attach_json_paths(crimes_by_city):
    """Create json paths for each potential city name"""
    crimes_by_city.json_paths = {}
    crimes_by_city.json_paths[crimes_by_city.fbi_city_name] = get_json_path(
        crimes_by_city.fbi_state, crimes_by_city.fbi_city_name)
    for city_name in crimes_by_city.alternate_city_names:
        crimes_by_city.json_paths[city_name] = get_json_path(
            crimes_by_city.fbi_state, city_name)
def get_json_path(state, city_name):
    """Generate a filename with characters that won't bork filesystems"""
    city_name = city_name.lower()
    city_name = re.sub(r"[']+", '', city_name)
    city_name = re.sub(r'[? ,/._()-]+', '-', city_name)
    city_name = re.sub(r'^-+|-+$', r'', city_name)
    city_name = ''.join([city_name, '.json'])
    state = state.lower()
    return os.path.join(state, city_name)
def timedelta_to_seconds(td):
    return td.days*24*3600 + td.seconds + td.microseconds/1e6

class GoogleMapsQueryDaemon(threading.Thread):
    def __init__(self, app, delay=35):
        self.app = app
        self.__queue = Queue.Queue(0)
        super(GoogleMapsQueryDaemon, self).__init__()
        self.last_google_query = datetime.utcnow() + timedelta(days=-1)
        self.delay = timedelta(seconds=abs(delay))
        self.googled = set()
    def run(self):
        while True:
            (crimes_by_city, city_name) = self.__queue.get()
            if crimes_by_city is None:
                return
            city_hash = "%s, %s" % (city_name, crimes_by_city.fbi_state)
            if city_hash in self.googled:
                print "Refusing to regoogle %s, %s" % (city_name,
                    crimes_by_city.fbi_state)
                continue
            self.googled.add(city_hash)
            time_diff = datetime.utcnow() - self.last_google_query
            time_sleep = max(0, timedelta_to_seconds(self.delay - time_diff))
            print "Googling %s, %s in %0.2f seconds" % (
                city_name, crimes_by_city.fbi_state, time_sleep)
            if time_diff < self.delay:
                time.sleep(time_sleep)
            city_json = self._do_google(crimes_by_city, city_name)
            self.last_google_query = datetime.utcnow()
    def google(self, crimes_by_city, city_name):
        """Put `city_name` from `crimes_by_city` into the queue"""
        self.__queue.put((crimes_by_city, city_name))
    def _do_google(self, crimes_by_city, city_name):
        """Actually google the city, write the result to a json file, and
        return the json"""
        state = crimes_by_city.fbi_state
        params = urllib.urlencode({
            'address':'%s, %s' % (city_name, state),
            'sensor':'false'})
        gmaps_request_url = ('http://maps.google.com/maps/api/geocode/json?%s' %
            (params))
        try:
            response = urllib2.urlopen(gmaps_request_url, timeout=5).read()
        except urllib2.URLError as e:
            print "GoogleMapsQueryDaemon: URLLIB ERROR", e
            response = json.dumps({'status':'OVER_QUERY_LIMIT'})
        else:
            json_outfile = os.path.join(self.app.options['json_dir'],
                crimes_by_city.json_paths[city_name])
            with open(json_outfile, 'w') as f:
                f.write(response)
        response_as_json = json.loads(response)
        if response_as_json['status'] == 'OVER_QUERY_LIMIT':
            print ("OVER_QUERY_LIMIT. Sleeping for 24 hours as of %s" %
                datetime.datetime.utcnow())
            time.sleep(24*3600)
        return response_as_json

class FBIDaemon(threading.Thread):
    def __init__(self, app):
        self.app = app
        super(FBIDaemon, self).__init__()
        self.__queue = Queue.PriorityQueue(0)
    def run(self):
        while True:
            (priority, crimes_by_city) = self.__queue.get()
            if crimes_by_city is None:
                self.app.google_daemon.google(None, None)
                return
            # dump "(and Other City)" from fbi_city_name
            city_name = crimes_by_city.fbi_city_name
            city_name = re.sub(r' ?\([^\)]*\)', '', city_name)
            jsonpath = os.path.join(self.app.options['json_dir'],
                crimes_by_city.json_paths[city_name])
            if not os.path.exists(jsonpath):
                self.app.google_daemon.google(crimes_by_city, city_name)
            # alternate names
            for alternate_name in crimes_by_city.alternate_city_names:
                jsonpath = os.path.join(self.app.options['json_dir'],
                    crimes_by_city.json_paths[alternate_name])
                if not os.path.exists(jsonpath):
                    self.app.google_daemon.google(crimes_by_city, alternate_name)

    def put(self, crimes_by_city, priority=1):
        """Priority 0 is highest"""
        self.__queue.put((priority, crimes_by_city))
