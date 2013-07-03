import os
import pdb
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.localflavor.us.us_states import US_STATES
from models import TheFeed,FallBacks
from django.db.models import Q
from django.conf import settings
import requests
import json
from itertools import chain, izip
'''
class RenderNewsFeed():

	def process_request(self,request):
		if request.is_ajax():
			try:
			 	city=request.GET['city']
			 	state=request.GET['state']
			 	data={
			 	'city':city,
			 	'state':state}

			 	for x in US_STATES:
			 		if x[1]==state:
			 			state=x[0]

	           
				try:
					query1=Q(active=True,city__icontains=city,state__exact=state)
					feed=TheFeed.objects.select_related().filter(query1)
					ct=feed.count()
					if ct == 0:
						request.session['backup']=True
						feed=FallBacks.objects.all()
				except TheFeed.DoesNotExist:
					feed=FallBacks.objects.all()

				fallbacks=FallBacks.objects.select_related().all()
				request.session['FallBacks']=fallbacks						
						

	  			if request.session.get('GeoFeedData',False):
	  				return HttpResponse()
	  			request.session['GeoFeedData']=feed
	  			return None
	  		except KeyError:
	  			pass 

	  	return None       

'''

class GetGeoIp():
	def process_request(self,request):
		if request.session.get('GeoFeedObjects',False):
			return None
		ip=request.META['REMOTE_ADDR']
		r=requests.get('http://freegeoip.net/json/')
		resp=r.json()
		city=resp['city']
		state_abbr=resp['region_code']
		state_long=resp['region_name']
		try:
			f=TheFeed.objects.filter(active=True,city=city,state=state_abbr).order_by('created').reverse()
			if f.count() == 0:
				request.session['backup']=True
				f=FallBacks.objects.select_related().all()
		except TheFeed.DoesNotExist:
			request.session['backup']=True
			f=FallBacks.objects.select_related().filter()

		try:
			no_visible=True
			a=TheFeed.objects.filter(visible_to_all=True).order_by('created').reverse()
			if a.count() == 0:
				no_visible=False
		except TheFeed.DoesNotExist:
			pass

		if no_visible:
			feed=list(chain(f,a))
		else:
			feed=f         
		request.session['GeoFeedObjects']=feed	
		


		return None



