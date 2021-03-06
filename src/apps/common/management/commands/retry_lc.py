import pdb
import requests
import logging
from django.conf import settings
settings.SITE_ID = 1
from django.core.management.base import BaseCommand, CommandError
from apps.contact.models import Lead
from apps.contact.views import post_to_leadconduit, send_conduit_error
TimeoutError = requests.exceptions.Timeout
logger = logging.getLogger('lead_conduit')

class Command(BaseCommand):
	help = 'retry all lead conduits requests that didnt succeed'

	def handle(self,*args,**options):
		leads = Lead.objects.filter(retry=True,date_created__gte='2013-10-23 15:24:42.386199')
		logger.info('About to retry %s leads' % leads.count())
		print 'about to retry %s leads' % leads.count()
		for x in leads:
			if x.call_now():
				logger.info('retrying %s' % x.name)
				print 'retrying {0}'.format(x.name)
				data = {
						'xxAccountId':settings.LEAD_ACCOUNT_ID,
		                'xxCampaignId':settings.LEAD_CAMPAIGN_ID,
		                'lead_id':x.id,
		              	'trusted_url':x.trusted_url,
		                'customername':x.name,
		                'phone':x.phone,
		                'email':x.email,
		                'formlocation':x.referer_page,
		                'agentid':x.agent_id,
		                'source':x.source,
		                'affkey':x.affkey,
		                'searchkeywords':x.search_keywords,
		                'searchengine':x.search_engine,
		                'ip':x.ip_address,
		                'device':x.device
						}
				logger.info('parameters sent were %s' % data)
				print 'parameters sent were {0}'.format(data)
				post_to_leadconduit(data,test=settings.LEAD_TESTING,retry=True)
			else:
				logger.info('%s not posting to lead conduit based on incorrect time' % x.name)
				print '%s not posting to lead conduit based on incorrect time' % x.name

