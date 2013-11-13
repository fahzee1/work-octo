import pdb
import csv
import requests
import logging
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from apps.contact.models import Lead

class Command(BaseCommand):
	help = 'retry all lead conduits requests that didnt succeed'

	def handle(self,*args,**options):
		first_line = ('Name', 'Email', 'Phone', 'Agent Id', 'Source', 'Affkey', 'Referer Page')
		since = datetime.date(2013,10,16)
		lead = Lead.objects.filter(date_created__gte=since)
		print 'getting ready to write %s to csv..'% lead.count()
		csv_file = open('/Users/cjogbuehi/virtualenvs/test.csv','wb')
		writer = csv.writer(csv_file)
		writer.writerow(first_line)
		for x in lead:
			values = (x.name,x.email,x.phone,x.agent_id,x.source,x.affkey,x.referer_page)
			writer.writerow(values)

		csv_file.close()
		print 'done...'

