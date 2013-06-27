import os
import pdb
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.localflavor.us.us_states import US_STATES
from models import TheFeed,FallBacks
from django.db.models import Q
from django.conf import settings
consumer_key=settings.TWITTER_CONSUMER_KEY
consumer_secret=settings.TWITTER_CONSUMER_SECRET
access_token=settings.TWITTER_ACCESS_TOKEN
access_secret=settings.TWITTER_ACCESS_TOKEN_SECRET

class RenderNewsFeed():

	def process_request(self,request):
		if request.is_ajax():
			try:
			 	city=request.GET['city']
			 	state=request.GET['state']
			 	data={
			 	'city':city,
			 	'state':state
	            }

	     
	     			for x in US_STATES:
	            			if x[1]==state:
	            				state=x[0]
	           
				try:
					query1=Q(active=True,city__icontains=city,state__exact=state)
					feed=TheFeed.objects.select_related().filter(query1)[:5]
					ct=feed.count()
					if ct == 0:
						request.session['backup']=True
						feed=FallBacks.objects.all()
				except TheFeed.DoesNotExist:
					feed=FallBacks.objects.all()[:5]

				fallbacks=FallBacks.objects.select_related().all()
				request.session['FallBacks']=fallbacks[:5]						
						

	  			if request.session.get('GeoFeedData',False):
	  				return HttpResponse()
	  			request.session['GeoFeedData']=feed
	  			return None
	  		except KeyError:
	  			pass 

	  	return None       