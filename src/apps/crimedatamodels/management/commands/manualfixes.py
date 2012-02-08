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
    help = "Fix weird city names that Real Humans manually discovered"
    option_list = BaseCommand.option_list + (
        make_option('-n', '--dry-run', action='store_true', default=False,
            dest='dry_run',
            help="Dry run; don't actually save changes to the DB"),
        make_option('-V', '--verbose', action='store_true', default=False,
            dest='verbose', help='talk about everything that happens'),
    )
    def handle(self, *args, **options):
        self.app = lambda: None # dummy object
        self.app.options = options
        self.fix_weird_city_names()
    def save(self, model_instance):
        if not self.app.options['dry_run']:
            model_instance.save()
    def fix_weird_city_names(self):
        weird_names = {
            ('Athens-clarke County', 'GA'): ('Athens-Clarke County', 'GA'),
            ('Avonmore Boro', 'PA'): ('Avonmore', 'PA'),
            ('St. Clair Boro', 'PA'): ('St. Clair', 'PA'),
            ('Louisville Metro', 'KY'): ('Louisville', 'KY'),
            ('Nunda Town And Village', 'NY'): ('Nunda', 'NY'),
            ('Carmel', 'CA'): ('Carmel-by-the-Sea', 'CA'),
            ('Wa Keeney', 'KS'): ('WaKeeney', 'KS'),
            ("Carney's Point Township", 'NJ'): ("Carney's Point", 'NJ'),
            ('De Ridder', 'LA'): ('DeRidder', 'LA'),
            ('Deland', 'FL'): ('DeLand', 'FL'),
            ('Mount Gretna Borough', 'PA'): ('Mount Gretna', 'PA'),
            ('Nazareth Area', 'PA'): ('Nazareth', 'PA'),
        }
        for ((o_name, o_state), (n_name, n_state)) in weird_names.iteritems():
            cities = CrimesByCity.objects.filter(fbi_city_name=o_name,
                fbi_state=o_state)
            if not cities:
                print "No CrimesByCity found for 'weird' name: %s, %s" % (
                    o_name, o_state)
            for city in cities:
                city.fbi_city_name = n_name
                city.fbi_state = n_state
                if self.app.options['verbose']:
                    print "Saving CrimesByCity: %s, %s --> %s, %s" % (
                        o_name, o_state, n_name, n_state)
                self.save(city)
        for ((o_name, o_state), (n_name, n_state)) in weird_names.iteritems():
            cities = CityLocation.objects.filter(city_name=o_name,
                state=o_state)
            if not cities:
                print "No CityLocation found for 'weird' name: %s, %s" % (
                    o_name, o_state)
            for city in cities:
                city.city_name = n_name
                city.state = n_state
                if self.app.options['verbose']:
                    print "Saving CityLocation: %s, %s --> %s, %s" % (
                        o_name, o_state, n_name, n_state)
                self.save(city)
