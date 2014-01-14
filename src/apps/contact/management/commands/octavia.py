import pdb
import csv
import requests
import logging
from optparse import make_option
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from apps.contact.models import CEOFeedback



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
    positives = CEOFeedback.objects.filter(feedback_type='positive')
    print positives.count()
    found = False
    empty = []
    i = 0
    for x in positives:
        if x.name == 'Heather Oney':
            found = True
        if found and i < 501:
            empty.append(x)
    print len(empty)

    csvfile = open(the_file, 'wb')
    writer = csv.writer(csvfile)
    for x in empty:
        values = (x.name, x.email)
        writer.writerow(values)

    csvfile.close()
    print 'done'



        
