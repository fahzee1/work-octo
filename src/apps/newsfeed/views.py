import pdb
import twitter
from models import TheFeed,FallBacks,TweetBackup
from django.http import HttpResponse, HttpResponseBadRequest,Http404
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
		    backups=TweetBackup.objects.all()
		    b_count=backups.count()
		    if b_count != 0:
			    _list=[]
			    for b in backups.values('text'):
				    _list.append(b['text'])
			    for t in tweets:
				    if t.text not in _list:
					    TweetBackup.objects.create(text=t.text,GetRelativeCreatedAt=t.GetRelativeCreatedAt())
			    for ba in backups:
				    ba.remove_old()	

		    else:
			    for t in tweets:
				    TweetBackup.objects.create(text=t.text,GetRelativeCreatedAt=t.GetRelativeCreatedAt())	

	    except:
		    tweets=TweetBackup.objects.all()
			
	if tweets:
	    return tweets[:5]
	else:
	    return None

def hourly_check(request):
	if request.is_ajax():
		feeds=TheFeed.objects.filter(active=True)
		for x in feeds:
			x.feed_expired()
		return HttpResponse()
	return HttpResponseBadRequest()



def render_feed(request):
    #ajax request
    ctx={}
    tweets=give_me_tweets()
    data=request.session.get('GeoFeedObjects',False)
    if data and tweets:
        results=list(chain.from_iterable(izip(data['Feed'],tweets)))
        for x in data['Feed']:
            for y in tweets:
                if y not in results:
                    results.append(y)
                if x not in results:
                    results.append(x)
    else:
    	try:
        	results=data['Feed']
        except KeyError:
        	raise Http404
    if results:    	
    	ctx['GeoFeed']=results
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



