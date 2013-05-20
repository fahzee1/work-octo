import csv
import os
import datetime
import settings

from django.core.management.base import BaseCommand, CommandError

from apps.testimonials.models import Textimonial

class Command(BaseCommand):
    help = 'Takes the fixture named new_pa_testimonials.csv and imports it'

    def handle(self, *args, **options):
    	# Using a static CSV file named 'new_pa_testimonials.csv' we import
    	# testimonials from the old protect america database.
    	# the rows are as follows
    	# row[0] = first_name
    	# row[1] = last_name
    	# row[2] = city
    	# row[3] = state
    	# row[4] = message
    	# row[5] = date (2005-01-06 14:38:33)

    	csv_file_path = os.path.join(settings.PROJECT_ROOT, 'src', 'apps', 
    		'testimonials', 'fixtures', 'new_pa_testimonials.csv')
    	reader = csv.reader(open(csv_file_path, 'r'),
    		delimiter=',', quotechar='"')

    	counter = 0
    	for row in reader:
    		if counter > 0:
	    		text = Textimonial()
	    		text.first_name = row[0]
	    		text.last_name = row[1]
	    		text.city = row[2]
	    		text.state = row[3]
	    		text.message = row[4]
	    		try:
	    			text.date_created = datetime.datetime.strptime(row[5],
	    				'%Y-%m-%d %H:%M:%S')
	    		except:
	    			text.date_created = datetime.datetime.strptime(
	    				'2012-01-01 12:12:12', '%Y-%m-%d %H:%M:%S')
	    		text.permission_to_post = True
	    		text.rating = 0
	    		text.email = ''
	    		text.save()
	    	counter = counter + 1
