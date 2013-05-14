import csv
import glob
from optparse import make_option
import os
import re
from string import capwords

from django.core.management.base import BaseCommand, CommandError

from apps.crimedatamodels.models import State, CrimesByCity, ZipCode

class Command(BaseCommand):
    help = "Populate the database with crime data from a csv file."
    option_list = BaseCommand.option_list + (
        make_option('-D', '--data-dir', dest='data_dir',
            help='Data directory where stripped crime data csv files can be '+
            'found. Crime data files should be named as '+
            'stripped-crime-data-`year`.csv where `year` is an actual year. '+
            'For example, stripped-crime-data-2008.csv. '+
            'The first line of the file should be column names and the '+
            'rest of the file should be csv rows.'),
        make_option('-V', '--verbose', action='store_true', default=False,
            dest='verbose', help='talk about everything that happens'),
    )

    def handle(self, *args, **options):
        if options['data_dir'] is not None:
            app = lambda: None # dummy object
            app.options = options
            crime_data_files = fetch_crime_data_files(options['data_dir'])
            for crime_data_file in crime_data_files:
                for city in parse_crime_data_csv(app, crime_data_file):
                    if options['verbose']:
                        print "Saving %s %s, %s" % (
                            city.entry['year'],
                            city.entry['fbi_city_name'],
                            city.entry['fbi_state'])
                    city.save_crimesbycity()
        else:
            raise CommandError("Missing args. See --help")
def parse_crime_data_csv(app, crime_data_file):
    """Read CSV file into unsaved CrimesByCity model instances"""
    if app.options['verbose']:
        print "Parsing CSV %s" % (crime_data_file['path'])
    with open(crime_data_file['path']) as file:
        reader = csv.DictReader(file)
        for entry in reader:
            entry['year'] = crime_data_file['year']
            fbi_entry = FBIData(entry)
            if fbi_entry.entry['state']:
                state = fbi_entry.entry['state']
                try:
                    current_state = State.objects.get(name=state)
                except State.DoesNotExist:
                    raise CommandError("Invalid US State name `%s` in %s" %
                        (state, crime_data_file['path']))
            fbi_entry.entry['fbi_state'] = current_state.abbreviation
            del fbi_entry.entry['state']
            if CrimesByCity.objects.filter(
                fbi_city_name=fbi_entry.entry['fbi_city_name'],
                fbi_state=current_state.abbreviation,
                year=fbi_entry.entry['year']
                ).count():
                if app.options['verbose']:
                    print "%s %s, %s already in database. Skipping." % (
                        fbi_entry.entry['year'],
                        fbi_entry.entry['fbi_city_name'],
                        fbi_entry.entry['fbi_state'])
                continue
            yield fbi_entry
class FBIDataError(Exception):
    pass
class FBIData(object):
    """Take an FBI csv entry, clean it up, and spit it out as a usable
    CrimesByCity"""
    def __init__(self, entry):
        cleaned_entry = self.massage_entry_fields(entry)
        self.verify_fields(cleaned_entry)
        self.entry = cleaned_entry
    def massage_entry_fields(self, entry):
        new_entry = dict()
        for (k, v) in entry.iteritems():
            if not k:
                continue
            k = re.sub(r'(\w)\d+', r'\1', k)
            k = re.sub(r'[ _-]+', r'_', k)
            k = k.lower()
            v = re.sub(r'(\d),', r'\1', v) # strip commas from long numbers
            v = re.sub(r'(\w),(\w)', r'\1, \2', v)
            v = re.sub(r'(\D)\d+', r'\1', v) # trailing footnote no. Illinois6
            v = re.sub(r'^\s+|\s$', r'', v) # v.strip()
            v = re.sub(r'[ ]{2,}', ' ', v) # strip double+ spaces
            v = capwords(v)
            v = re.sub(r'\bOf\b', 'of', v)
            if k == 'city':
                k = 'fbi_city_name'
            if k not in ('fbi_city_name',) and v == '':
                v = None
            if k == 'population' and (v is None or v == '0'):
                v = 1
            new_entry[k] = v
        return new_entry
    def verify_fields(self, entry):
        """Raise an exception if a field in `entry` is invalid"""
        if not entry['fbi_city_name']:
            raise FBIDataError("Record without fbi_city_name: %r" % entry)
    def save_crimesbycity(self):
        """Save the FBI data to a CrimesByCity record"""
        crimes_by_city = CrimesByCity(**self.entry)
        crimes_by_city.save()

def fetch_crime_data_files(data_dir):
    crime_data_files = []
    for file in sorted(glob.glob(os.path.join(data_dir,
        'stripped-crime-data-*.csv'))):
        try:
            year = re.search(r'stripped-crime-data-(\d{4})\.csv', file).group(1)
        except (AttributeError, IndexError) as err:
            raise CommandError("Bad crime data file name: %s" % file)
        crime_data_files.append({'path':file, 'year':year})
    return crime_data_files
