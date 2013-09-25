import csv
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apps.contact.models import Lead 
from glob import glob
from datetime import datetime


class Command(BaseCommand):
	help = 'Script used to extract date, lead id, and disposition from csv and get associated gclid to send to google'
	option_list = BaseCommand.option_list + (
        make_option('--ofile', dest='output_file',
            help='destination where to create new csv'
            ),
        make_option('--ifile', dest='csv_file',
            help='destination where to find csv'
            ),
        make_option('--verbose', dest='verbose',
            help='Print to the screen'
            ),
        )

	def handle(self, *args, **options):
		app = lambda : None
		app.options = options
		if not options['output_file'] and not options['csv_file']:
			raise CommandError('Need either csv file location or location to create file')
		else:
			csv_data = get_csv_data(app,options['csv_file'])
			write_data = write_csv_data(app,options['output_file'],csv_data)




def create_correct_date(string):
	obj = datetime.strptime(string,'%m/%d/%Y:%H:%M:%S')
	return str(obj)

def get_csv_data(app,_file):
	data = []
	if app.options['verbose']:
		print 'opening csv file...'
	with open(_file,'rb') as csvfile:
		reader = csv.Dictreader(csvfile)
		have_gclid = False
		for info in reader:
			csv_dict = {}
			try:
				lead = Lead.objects.get(id=info['lead_id'])
				if lead.gclid:
					have_gclid = True
			except Lead.DoesNotExist:
				lead = None

			csv_dict['lead_found'] = (True if lead else False)
			csv_dict['date'] = create_correct_date(info['date'])
			csv_dict['disposition'] = info['disposition']
			csv_dict['lead_id'] = info['lead_id']
			csv_dict['gclid'] = (lead.gclid if have_gclid else None)
			data.append(csv_dict)

	return data

def write_csv_data(app,the_file,data):
	if app.options['verbose']:
		print 'writing data to csv with GCLID..'
	first_line = 'Parameters:EntityType=OFFLINECONVERSION;TimeZone=%s;' % time_zone
	second_line = ('Action','Google Click','Conversion Name','Conversion Value','Conversion Time')

	csv = open(the_file,'wb')
	writer = csv.writer(csv)
	writer.writerow(first_line)
	writer.writerow(second_line)
	for line in data:
		row_values = ('add',line['gclid'],line['disposition'],line['value if one'],line['date'])
		writer.writerow(row_values) 
	csv.close()
	if app.options['verbose']:
		print 'CSV ready my boy....!'





