import re
import urls
import urllib
import urllib2
import operator
import random
from django.http import Http404
from decimal import Decimal
from datetime import datetime, timedelta

from urllib import urlencode
from django.db.models import Q
import twitter
from django.contrib.localflavor.us.us_states import US_STATES
from django.core.urlresolvers import reverse, resolve
from django.core.cache import cache
from django.views.decorators.cache import cache_page, never_cache

from django.shortcuts import render_to_response,render,redirect
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, \
    HttpResponsePermanentRedirect, HttpResponseBadRequest
from django.utils import simplejson
from django.utils.cache import patch_vary_headers
from django.contrib.sites.models import Site

from apps.contact.forms import LeadForm, AffiliateLongForm
from apps.affiliates.models import Affiliate
from apps.common.forms import LinxContextForm
from apps.news.models import Article
from apps.pricetable.models import Package
from apps.newsfeed.models import TheFeed,FallBacks
from itertools import chain, izip
from django.core.mail import send_mail

consumer_key=settings.TWITTER_CONSUMER_KEY
consumer_secret=settings.TWITTER_CONSUMER_SECRET
access_token=settings.TWITTER_ACCESS_TOKEN
access_secret=settings.TWITTER_ACCESS_TOKEN_SECRET


def redirect_wrapper(request, agent_id):
    get = request.GET.copy()
    get['agent'] = agent_id

    try:
        affiliate = Affiliate.objects.get(agent_id=agent_id.lower())
        request.session['refer_id'] = affiliate.agent_id
    except Affiliate.DoesNotExist:
        if request.META['PATH_INFO'][-1] != '/':
            resolved = resolve(request.META['PATH_INFO'] + '/')
            if resolved.url_name != 'apps.common.views.redirect_wrapper':
                return HttpResponseRedirect(reverse(resolved.url_name))

    return HttpResponseRedirect('/?%s' % urlencode(get))


def thank_you(request, custom_url=None):
    agent_id = request.COOKIES.get('refer_id', None)
    affiliate_obj = None
    try:
        affiliate_obj = Affiliate.objects.get(agent_id=agent_id)
    except Affiliate.DoesNotExist:
        pass

    # until the new lead system is ready go ahead and manually redirect
    # to new landing page here
    if affiliate_obj and affiliate_obj.thank_you and not custom_url:
        url = '/thank-you%s' % affiliate_obj.thank_you
        if 'leadid' in request.GET:
            url = url + '?leadid=%s' % request.GET['leadid']
        return HttpResponseRedirect(url)

    c = {'page_name': 'thank-you',
         'custom_url': custom_url,
         'affiliate_obj': affiliate_obj}
    return simple_dtt(request, 'thank-you/index.html', c)


def clear_my_cookies(request):
    response = render_to_response('support/clear-my-cookies.html',
        {}, context_instance=RequestContext(request))
    response.delete_cookie('refer_id', domain='.protectamerica.com')
    response.delete_cookie('affkey', domain='.protectamerica.com')
    response.delete_cookie('source', domain='.protectamerica.com')
    return response


def fivelinxcontest(request):
    if request.method == 'POST':
        form = LinxContextForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/contest/thanks/')
    else:
        form = LinxContextForm()
    c = {'form': form, 'page_name': 'contest'}
    return simple_dtt(request, 'affiliates/five-linx/contest.html', c)


def fivelinxwinner(request):
    from apps.common.models import LinxContext
    winner = LinxContext.objects.order_by('?')
    return HttpResponse('%s' % winner[0])


def get_active(urllist, name, pages=None):
    if pages is None:
        pages = []
    for entry in urllist:
        try:
            pname = entry.default_args['extra_context']['page_name']
            if pname == name:
                pages.append(pname)
                return get_active(urllist, entry.default_args['extra_context']['parent'], pages)
        except:
            pass
    return pages


def simple_dtt(request, template, extra_context, expire_days=90):
    expire_time = timedelta(days=expire_days)

    if 'pages' in extra_context:
        pages = extra_context['pages']
        pages.append(extra_context['page_name'])
    else:
        pages = get_active(urls.urlpatterns, extra_context['page_name'])

    #handle special page cases for phone number
    #if extra_context['page_name'] == 'agent-two':
        #extra_context['phone_number'] = '1-888-951-5156'

    forms = {}
    forms['basic'] = LeadForm()
    forms['long'] = AffiliateLongForm()

    extra_context['forms'] = forms
    extra_context['active_pages'] = pages

    extra_context['affkey'] = request.session.get('affkey')

    affiliate = request.COOKIES.get('refer_id', None)
    newaffiliate = None
    if not affiliate and 'agent_id' in extra_context:
        newaffiliate = extra_context['agent_id']

    if newaffiliate:
        request.session['refer_id'] = newaffiliate

    visited_pages = request.session.get('vpages', [])
    if extra_context['page_name'] not in visited_pages:
        visited_pages.append(extra_context['page_name'])
        request.session['vpages'] = visited_pages

    response = render(request,template,extra_context)
    patch_vary_headers(response, ('Host',))
    return response


def payitforward(request):

    videos = []
    videos.append({
        'charity': 'Hosanna House',
        'team': 'MSU Team: Movement Advertising',
        'url': 'http://www.youtube.com/watch?v=z9VxKbxjNsU',
    })
    videos.append({
        'charity': 'Help A Willing Kid',
        'team': 'MSU Team: Top Hat Media',
        'url': 'http://vimeo.com/38477884',
    })
    videos.append({
        'charity': 'Beekman Therapeutic Riding Center',
        'team': 'MSU Team: Five Star Media',
        'url': 'http://www.youtube.com/watch?v=IyR82vQDAKA',
    })
    videos.append({
        'charity': 'For Better Independence',
        'team': 'MSU Team: Inifinite Solutions',
        'url': 'http://www.youtube.com/watch?v=lAGzVtBliCo',
    })
    videos.append({
        'charity': 'Pay It Forward Challenge',
        'team': 'Protect America',
        'url': 'http://www.youtube.com/watch?v=HFhmcJiIZtQ',
    })

    forms = {}
    forms['basic'] = LeadForm()

    if request.method == "POST":
        form = PayItForwardForm(request.POST)
        if form.is_valid():
            formset = form.save(commit=False)
            formset.save()
            formset.email_shawne()

    else:
        form = PayItForwardForm()

    return render_to_response('payitforward.html',
        {
            'page_name': 'payitforward',
            'forms': forms,
            'videos': videos,
        }, context_instance=RequestContext(request))


@cache_page(60 * 60 * 4)
def index(request):
    return index_render(request, 'index.html', {})


@cache_page(60 * 60 * 4)
def index_test(request, test_name):
    if test_name == 'packages':
        template = 'tests/index-with-packages.html'
    if test_name == 'advantage':
        template = 'tests/test-advantage.html'
    elif test_name == 'price':
        template = 'tests/index-with-price.html'
    elif test_name == 'concept':
        template = 'tests/index-concept.html'
    elif test_name == 'packages-price':
        template = 'tests/index-with-price-and-packages.html'
    elif test_name == 'best-deal':
        template = 'tests/index-with-best-deal.html'
    else:
        return redirect('home')

    return index_render(request, template, {})


def index_render(request, template, context):
    context['page_name'] = 'index'
    context['pages'] = ['index']

    latest_news = Article.objects.order_by('-date_created')[:3]
    context['latest_news'] = latest_news
    try:
        tweets = cache.get('TWEETS')
        if tweets is None:
            t_api = twitter.Api(consumer_key=consumer_key,
                                consumer_secret=consumer_secret,
                                access_token_key=access_token,
                                access_token_secret=access_secret)
            tweets = t_api.GetUserTimeline('protectamerica',count=3)
            cache.set('TWEETS', tweets, 60*60)
        context['tweets'] = tweets[:3]
    except:
        context['tweets'] = []

    check_agent = request.GET.get('agent', None)
    if check_agent == 'a01986':
        return HttpResponseRedirect("/affiliate/a01986/?agent=a01986")
    elif check_agent == 'a02675':
        return HttpResponseRedirect("/affiliate/a02675/?agent=a02675")
    elif check_agent == 'a03053':
        return HttpResponseRedirect("/affiliate/a03053/?agent=a03053")

    if 'no_mobile' in request.GET:
        request.session['no_mobile'] = True
    
    return simple_dtt(request, template, context)




def family_of_companies(request):
    ctx = {}
    ctx['page_name'] = 'family'
    ctx['pages'] = ['about-us']
    
    family_json_obj = cache.get('FAMILYJSON')
    if family_json_obj is None:
        try:
            family_json_url = 'http://media.quickenloans.com/threadnation/public/companies.json'
            family_data = urllib2.urlopen(family_json_url)
            family_json_obj = simplejson.loads(family_data.read())
        except:
            return None
        if 'Error' in family_json_obj:
            return None

        cache.set('FAMILYJSON', family_json_obj, 60*60*60)

    # group by industry
    industry_dict = {}
    for family in family_json_obj:
        if family['industry'] not in industry_dict:
            industry_dict[family['industry']] = []
        industry_dict[family['industry']].append(family)

    ctx['industries'] = industry_dict
    return simple_dtt(request, 'about-us/family-of-companies.html', ctx)


def black_friday(request):
    ctx = {}
    ctx['page_name'] = 'index'
    ctx['black_friday_delta'] = datetime(2013, 11, 29) - datetime(
        datetime.today().year, datetime.today().month, datetime.today().day)
    return simple_dtt(request, 'external/black-friday/index.html', ctx)

def black_friday_ajax(request):
    from models import BlackFriday
    submission = BlackFriday()
    if request.method != "POST":
        return HttpResponseRedirect('/')
    email = request.POST.get('email',None)
    if email:
        submission.email = email
        submission.save()
        subject = 'Black Friday Subscriber!'
        message = 'Hey Caroline,\n\tYour new black friday subscriber is %s.\n\n From CJ :)' % email
        too = 'caroline@protectamerica.com'
        from_email = 'Protect America <noreply@protectamerica.com>'
        send_mail(subject,message,from_email,[too])
        return HttpResponse()
    return HttpResponseBadRequest()
