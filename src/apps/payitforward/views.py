from apps.payitforward.models import Organization
from apps.common.views import simple_dtt
from django.utils import simplejson
from django.conf import settings
from django.shortcuts import render ,redirect
from apps.newsfeed.views import give_me_tweets



def point_tracking(request):
    org_data = []
    for org in Organization.objects.all():
        org_data.append((org.points(), '<img src="%s%s" height="48px" />' % (settings.MEDIA_URL, org.image), '%s' % org.color ))

    return simple_dtt(request, 'payitforward/point-tracking.html', {
            'org_data': simplejson.dumps(org_data),
            'page_name': 'payitforward-point-tracking',
            'agent_id': 'i03237',
        })


def view_tweets(request):
	ctx = {}
	tweets = give_me_tweets(payitforward=(not settings.DEBUG))
	ctx['tweets'] = tweets
	return render(request,'payitforward/tweets.html',ctx)