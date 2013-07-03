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


def give_me_tweets():
	tweets=cache.get('TWEETS')
	if not tweets:
		try:
			t_api=twitter.Api(consumer_key=consumer_key,
				              consumer_secret=consumer_secret,
				              access_token_key=access_token,
				              access_token_secret=access_secret)
			tweets=t_api.GetUserTimeline('protectamerica')
			cache.set('TWEETS',tweets,60*60)
		except:
			pass

	return tweets

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

	tweets=give_me_tweets()

	results=list(chain.from_iterable(izip(fbacks,tweets[:5])))
	for x in fbacks:
		for y in tweets:
			if y not in results:
				results.append(y)
			if x not in results:
				results.append(x)
	ctx={'FallBacks':results}                  
	return render(request,'newsfeed/fallback.html',ctx)



def render_feed(request):
    #ajax request
    ctx={}
    tweets=give_me_tweets()
    data=request.session.get('GeoFeedData',False)
    fback=request.session.get('FallBacks',False)
    if data or fback:
        if tweets:
            results=list(chain.from_iterable(izip(data,tweets[:5])))
            for x in data:
                for y in tweets:
                    if y not in results:
                        results.append(y)
                    if x not in results:
                        results.append(x)
        else:
            results=data
        ctx['GeoFeed']=results
        ctx['FallBacks']=fback
    return render(request,'newsfeed/feed.html',ctx)


def nongeo_feed(request):
	ctx={}
	tweets=give_me_tweets()[:5]
	data=cache.get('NonGeoFeedData')
	if not data:
		data=TheFeed.objects.filter(active=True).order_by('created').reverse()[:5]
		if data.count() == 0:
			request.session['backup']=True
			data=FallBacks.objects.all()
		cache.set('NonGeoFeedData',data)

	results=list(chain.from_iterable(izip(data,tweets)))
	for x in data:
		for y in tweets:
			if y not in results:
				results.append(y)
			if x not in results:
				results.append(x)

	ctx['GeoFeed']=results
	return render(request,'newsfeed/feed.html',ctx)



