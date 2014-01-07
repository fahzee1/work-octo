import pdb
import twitter
from random import shuffle
from models import TheFeed,FallBacks,TweetBackup
from django.http import HttpResponse, HttpResponseBadRequest,Http404
from django.shortcuts import render , redirect
from itertools import chain, izip
from django.core.cache import cache
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db import transaction

consumer_key=settings.TWITTER_CONSUMER_KEY
consumer_secret=settings.TWITTER_CONSUMER_SECRET
access_token=settings.TWITTER_ACCESS_TOKEN
access_secret=settings.TWITTER_ACCESS_TOKEN_SECRET

@transaction.commit_manually
def give_me_tweets(payitforward=False,term=None):
	"""
	If for payitforward page fetch tweets with payitforward hashtags.
	If not fetch all posted PA Tweets.
	Regardless of the above two, check cache first for tweets.
	If we get any error along the way or no tweets return TweetBackups.

	Tranactions are being manually handled to stop duplicate Tweet backups
	from being created. If a duplicate or any type of error happens, 
	rollback the commit

	TODO maybe change order of operations like first cache, second backups,
	then finally make api call 
	"""

	search_results = None
	tweets = None
	backups=TweetBackup.objects.all()
	b_count=backups.count()
	for ba in backups:
		ba.remove_old()
	_list = [b for b in backups.values('text')]

	# authenticate with twitter, if fail get and return backups
	try:
		t_api=twitter.Api(consumer_key=consumer_key,
					      consumer_secret=consumer_secret,
					      access_token_key=access_token,
					      access_token_secret=access_secret,
					      requests_timeout=10)
	except:
		if payitforward:
			search_results = backups.filter(payitforward=True)
			transaction.rollback()
			return search_results
		else:
			tweets = backups.objects.all()
			shuffle(list(tweets))
			transaction.rollback()
			return tweets[:5]

	# if we're getting tweets for payitforward
	if payitforward:
		if not term:
			term = '#payitforwardMSU OR #payitforwardUFL OR #payitforwardUSA OR #payitforwardPA'
		search_results = cache.get('PAYITFOWARD_TWEETS')
		if not search_results:
			search_results = t_api.GetSearch(term=term)
			if search_results:
				cache.set('PAYITFOWARD_TWEETS',search_results,60*60)
				if b_count != 0:
					#got items in db so create backups and do duplicate checks
					for status in search_results:
						if status.text not in _list:
							try:
								TweetBackup.objects.create(text=status.text,
									                       GetRelativeCreatedAt=status.relative_created_at,
									                       payitforward=True,
									                       location=status.location)
							except IntegrityError:
							#trying to create duplicate record
								transaction.rollback()
							else:
								transaction.commit()
				else:
					#no items so create backups, should only ever be ran once
					for status in search_results:
						try:
							TweetBackup.objects.create(text=status.text,
								                       GetRelativeCreatedAt=status.relative_created_at,
								                       payitforward=True,
								                       location=status.location)
						except:
							#trying to create duplicate record
							transaction.rollback()
						else:
							transaction.commit()
			else:
				search_results = backups.filter(payitforward=True)


	# if we're just getting recent tweets
	else:
		tweets = cache.get('TWEETS')
		if not tweets:
			tweets = t_api.GetUserTimeline('protectamerica')
			cache.set('TWEETS',tweets,60*60)
			if b_count != 0:
				for t in tweets:
					if t.text not in _list:
						try:
							TweetBackup.objects.create(text=t.text,
								                      GetRelativeCreatedAt=t.GetRelativeCreatedAt(),
								                      location=t.location)
						except IntegrityError:
						#trying to create duplicate record
							transaction.rollback()
						else:
							transaction.commit()	
			else:
				for t in tweets:
					try:
						TweetBackup.objects.create(text=t.text,
							                      GetRelativeCreatedAt=t.GetRelativeCreatedAt(),
							                      location=t.location)
					except IntegrityError:
					#trying to create duplicate record
						transaction.rollback()
					else:
						transaction.commit()	

				
	# return based on what we're using
	if payitforward and search_results:
		transaction.commit()
		return search_results

	elif not payitforward and tweets:
		transaction.commit()
		return tweets[:5]

	else:
		transaction.rollback()
		return []



def hourly_check(request):
	if request.is_ajax():
		feeds=TheFeed.objects.filter(active=True)
		for x in feeds:
			x.feed_expired()
		return HttpResponse()
	return HttpResponseBadRequest()



def render_feed(request):
	#this has been shut off for now
	return redirect('home')


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


class LatestTwitterFeed(Feed):
	title = "Payitfoward Hashtag Tweets"
	description = "Protect Americas lastest Payitfoward tweets"
	link = ""

	def items(self):
		return TweetBackup.objects.all()




