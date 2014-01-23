import pdb
import re
from apps.payitforward.models import Organization
from apps.common.views import simple_dtt
from django.utils import simplejson
from django.utils.html import urlize
from django.conf import settings
from django.shortcuts import render ,redirect
from apps.newsfeed.views import give_me_tweets
from apps.newsfeed.models import TweetBackup
from random import choice
from django.views.decorators.cache import cache_page



def point_tracking(request):
    org_data = []
    for org in Organization.objects.all():
        org_data.append((org.points(), '<img src="%s%s" height="48px" />' % (settings.MEDIA_URL, org.image), '%s' % org.color ))

    return simple_dtt(request, 'payitforward/point-tracking.html', {
            'org_data': simplejson.dumps(org_data),
            'page_name': 'payitforward-point-tracking',
            'agent_id': 'i03237',
        })

@cache_page(60 * 60 * 4)
def view_tweets(request):
    ctx = {}
    tweetsMSU = []
    tweetsUFL = []
    tweetsUSA = []
    backups = TweetBackup.objects.filter(payitforward=True)
    #tweets = give_me_tweets(payitforward=(not settings.DEBUG))
    tweets = give_me_tweets(payitforward=True)
    if tweets:
        for tweet in tweets:
            tweet.text = urlize(tweet.text)
            if 'MSU' in tweet.text:
                if tweet not in tweetsMSU:
                    tweetsMSU.append(tweet)
            if 'UFL' in tweet.text:
                if tweet not in tweetsUFL:
                    tweetsUFL.append(tweet)
            if 'USA' in tweet.text:
                if tweet not in tweetsUSA:
                    tweetsUSA.append(tweet)


    if not tweetsUSA:
        tweetsUSA = TweetBackup.get_payitforward('USA')
    if not tweetsUFL:
        tweetsUFL = TweetBackup.get_payitforward('UFL')
    if not tweetsMSU:
        tweetsMSU = TweetBackup.get_payitforward('MSU')



    ctx['tweetsMSU'] = (tweetsMSU[:5] if tweets else None)
    ctx['tweetsUFL'] = (tweetsUFL[:5] if tweets else None)
    ctx['tweetsUSA'] = (tweetsUSA[:5] if tweets else None)
    ctx['agent_id'] = 'i03237'
    return render(request,'payitforward/payitforward.html',ctx)