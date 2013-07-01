from models import TheFeed
from django.http import HttpResponse



def hourly_check(request):
	if request.is_ajax():
		feeds=TheFeed.objects.filter(active=True)
		for x in feeds:
			x.feed_expired()
		return HttpResponse()
