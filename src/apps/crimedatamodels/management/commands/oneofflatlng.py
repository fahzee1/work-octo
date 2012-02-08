"""
Associate CrimesByCity instances to CityLocation instances by prompting a human
"""
from collections import namedtuple, deque
import csv
import decimal
import json
import math
from optparse import make_option
import os
import Queue
import re
import rlcompleter # to jazz up readline
import readline # to jazz up raw_input
from string import capwords
import sys
import threading

from django.core.management.base import BaseCommand, CommandError

from apps.crimedatamodels.models import State, CrimesByCity, ZipCode, CityLocation

class Command(BaseCommand):
    help = "Associate CrimesByCity instances with City instances using Google Maps"
    option_list = BaseCommand.option_list + (
        make_option('-l', '--latlng', dest='latlngfile',
            help='File of cities that originally needed latlng info'),
        make_option('-V', '--verbose', action='store_true', default=False,
            dest='verbose', help='talk about everything that happens'),
    )

    def handle(self, *args, **options):
        if options['latlngfile'] is not None:
            app = lambda: None # dummy object
            app.options = options

            with open(app.options['latlngfile']) as f:
                reader = csv.DictReader(f)
                for entry in reader:
                    location = CityLocation.objects.filter(city_name=entry['fbi_city_name'], state=entry['fbi_state']).get()
                    s = "INSERT INTO citylocations (city_name, state, latitude, longitude) VALUES ('%s', '%s', '%010.6f', '%010.6f');" % (location.city_name, location.state, location.latitude, location.longitude)
                    print s
