import pdb
import csv
import requests
import logging
from optparse import make_option
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from apps.contact.models import Lead

ids = [
"169263",
"169264",
"169265",
"169266",
"169267",
"169268",
"169269",
"169271",
"169273",
"169275",
"169276",
"169277",
"169279",
"169281",
"169282",
"169283",
"169293",
"169296",
"169297",
"169304",
"169305",
"169314",
"169316",
"169324",
"169343",
"169352",
"169358",
"169368",
"169373",
"169374",
"169489",
"169493",
"169494",
"169495",
"169502",
"169504",
"169512",
"169513",
"169520",
"169521",
"169527",
"169530",
"169532",
"169533",
"169534",
"169535",
"169536",
"169550",
"169555",
"169560",
"169568",
"169572",
"169573",
"169579",
"169580",
"169583",
"169586",
"169593",
"169595",
"169609",
"169610",
"169613",
"169725",
"169744",
"169748",
"169750",
"169754",
"169756",
"169757",
"169758",
"169760",
"169762",
"169763",
"169764",
"169765",
"169766",
"169767",
"169770",
"169775",
"169785",
"169790",
"169793",
"169796",
"169797",
"169798",
"169800",
"169803"
 ]

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--ofile', dest='output_file'),
        )

    def handle(self, *args, **options):
        if not options['output_file']:
            raise CommandError('Need output file')
        else:
           get_and_write_data(options['output_file'])






def get_and_write_data(the_file):
    print 'start filtering through %s ids...' % len(ids)
    csvfile = open(the_file,'wb')
    writer = csv.writer(csvfile)
    line = ('Lead ID','IP Address')
    writer.writerow(line)
    for id in ids:
        try:
            lead = Lead.objects.get(id=id)
            values = (id.decode("utf-8"), lead.ip_address.decode("utf-8"))
            writer.writerow(values)
            print 'done writing %s and %s to file' % (id,lead.ip_address)
        except Lead.DoesNotExist:
            print 'lead id %s not found' % id
            continue

    csvfile.close()
    print 'done!!!!!'





