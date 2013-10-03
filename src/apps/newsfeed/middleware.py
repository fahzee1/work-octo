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


class GetGeoIp():
	def process_request(self,request):
		if request.session.get('GeoFeedObjects',False):
			return None

		ip = False
		city = state_abbr = state_long = ip
		ip = request.META['REMOTE_ADDR']
		r = requests.get('http://freegeoip.net/json/'+ip)
		try:
			#if they return 403 response will get JSONDecode error here
			resp = r.json()
			city = resp['city']
			state_abbr = resp['region_code']
			state_long = resp['region_name']
			try:
				f = TheFeed.objects.filter(active=True,city=city,state=state_abbr).order_by('created').reverse()
				if f.count() == 0:
					f = FallBacks.objects.select_related().all()
			except TheFeed.DoesNotExist:
				f = FallBacks.objects.select_related().all()

		except:
			f = FallBacks.objects.select_related().all()

		try:
			no_visible = True
			a = TheFeed.objects.filter(active=True,visible_to_all=True).order_by('created').reverse()
			if a.count() == 0:
				no_visible = False
		except TheFeed.DoesNotExist:
			pass

		if no_visible:
			feed = list(chain(f,a))
		else:
			feed = f 
		FeedObjects = {}
		FeedObjects['Feed'] = feed
		if ip:
			FeedObjects['geo-ip'] = ip
		if city:
			FeedObjects['geo-city'] = city
		if state_abbr and state_long:
			FeedObjects['geo-state-abbr'] = state_abbr
			FeedObjects['geo-state-long'] = state_long

		request.session['GeoFeedObjects'] = FeedObjects	
		


		return None



