import csv
import pdb
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
        make_option('--time', dest='time_zone',
            help='destination where to find csv'
            ),
        )

    def handle(self, *args, **options):
        app = lambda : None
        app.options = options
        if not options['output_file'] and not options['csv_file']:
            raise CommandError('Need either csv file location or location to create file')
        else:
            if options['time_zone']:
                time_zone = options['time_zone']
            else:
                time_zone = '-0500'
            csv_data = get_csv_data(app,options['csv_file'])
            write_data = write_csv_data(app,options['output_file'],csv_data,time_zone)




def create_correct_date(string):
    if string != 'NULL':
        obj = datetime.strptime(string,'%m/%d/%y %H:%M ')
        obj = obj.strftime('%0m/%d/%Y %H:%M:%S %p')
    else:
        obj = 'NULL'
    return str(obj)

def get_csv_data(app,_file):
    data = []
    if app.options['verbose']:
        print 'opening csv file...'
    with open(_file,'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        have_gclid = False
        for info in reader:
            csv_dict = {}
            if info['Disposition'] == 'SOLD':
                try:
                    if info['Lead_Id'].isdigit():
                        lead = Lead.objects.get(id=info['Lead_Id'])
                        if lead.gclid:
                            have_gclid = True
                    else:
                        lead = None
                except Lead.DoesNotExist:
                    lead = None

                if 'DCS' in info['CreditResponse']:
                    value = 0
                else:
                    value = (float(info['MonitoringRate']) * 36) + (int(info['AdditionalEquipment'] if isinstance(info['AdditionalEquipment'],int) else float(info['AdditionalEquipment'])))
                csv_dict['lead_found'] = (True if lead else False)
                csv_dict['date'] = info['DispositionDate']
                csv_dict['disposition'] = info['Disposition']
                csv_dict['lead_id'] = info['Lead_Id']
                csv_dict['credit_response'] = info['CreditResponse']
                if lead:
                    csv_dict['gclid'] = lead.gclid
                else:
                    csv_dict['gclid'] = None
                csv_dict['conversion_value'] = value
                data.append(csv_dict)

    return data

def write_csv_data(app,the_file,data,time_zone):
    if app.options['verbose']:
        print 'writing data to csv with GCLID..'
    first_line = 'Parameters:EntityType=OFFLINECONVERSION;TimeZone=%s;' % time_zone
    second_line = ('Action','Google Click Id','Conversion Name','Conversion Value','Conversion Time')

    csv_file = open(the_file,'wb')
    writer = csv.writer(csv_file)
    writer.writerow([first_line])
    writer.writerow(second_line)
    for line in data:
        if line['gclid'] is None or line['gclid'] == '' or line['conversion_value'] == 0:
            continue
        row_values = ('add',line['gclid'],'Lead Sold',line['conversion_value'],line['date'])
        writer.writerow(row_values) 
    csv_file.close()
    if app.options['verbose']:
        print 'CSV ready my boy....!'






