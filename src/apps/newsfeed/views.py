import twitter
from models import TheFeed,FallBacks
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render 
from itertools import chain, izip
from django.core.cache import cache
from django.conf import settings
consumer_key=settings.TWITTER_CONSUMER_KEY
consumer_secret=settings.TWITTER_CONSUMER_SECRET
access_token=settings.TWITTER_ACCESS_TOKEN
access_secret=settings.TWITTER_ACCESS_TOKEN_SECRET




def hourly_check(request):
	if request.is_ajax():
		feeds=TheFeed.objects.filter(active=True)
		for x in feeds:
			x.feed_expired()
		return HttpResponse()
	return HttpResponseBadRequest()


def get_fallback(request):
	try:
		fbacks=request.session['FallBacks']
	except KeyError:
		fbacks=FallBacks.objects.select_related().all()

	tweets = cache.get('TWEETS')
    	if not tweets:
            t_api = twitter.Api(consumer_key=consumer_key,
                                consumer_secret=consumer_secret,
                                access_token_key=access_token,
                                access_token_secret=access_secret)
            tweets = t_api.GetUserTimeline('protectamerica',count=5)
            cache.set('TWEETS', tweets, 60*60)

	results=list(chain.from_iterable(izip(fbacks,tweets[:5])))
	for x in fbacks:
		for y in tweets:
			if y not in results:
				results.append(y)
			if x not in results:
				results.append(x)
	ctx={'FallBacks':results}                  
	return render(request,'newsfeed/fallback.html',ctx)
