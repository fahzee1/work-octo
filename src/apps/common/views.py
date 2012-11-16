import re
import urls
import urllib
import urllib2
from datetime import datetime, timedelta
from urllib import urlencode
import twitter
import operator
from decimal import Decimal

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse, resolve
from django.views.generic.simple import redirect_to
from django.utils import simplejson
from django.utils.cache import patch_vary_headers

from apps.contact.forms import LeadForm, AffiliateLongForm 
from apps.affiliates.models import Affiliate
from apps.common.forms import LinxContextForm
from apps.news.models import Article
from apps.pricetable.models import Package

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
        url = '/thank_you%s' % affiliate_obj.thank_you
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
    c = {'form': form,'page_name':'contest'}
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

def simple_dtt(request, template, extra_context):
    expire_time = timedelta(days=90)

    if 'pages' in extra_context:
        pages = extra_context['pages']
        pages.append(extra_context['page_name'])
    else:
        pages = get_active(urls.urlpatterns, extra_context['page_name'])

    forms = {}
    forms['basic'] = LeadForm()
    forms['long'] = AffiliateLongForm()
    
    extra_context['forms'] = forms
    extra_context['active_pages'] = pages

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

    response = render_to_response(template,
                              extra_context,
                              context_instance=RequestContext(request))
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
    if test_name == 'tcr-first':
        template = 'tests/top-consumer-test.html'
    elif test_name == 'promotion-first':
        template = 'tests/promotion-tcr-banner-test.html'
    elif test_name == 'nav-shop':
        template = 'tests/test-nav-shop.html'
    elif test_name == 'nav-pricing':
        template = 'tests/test-nav-pricing.html'
    elif test_name == 'nav-plans':
        template = 'tests/test-nav-plans.html'
    elif test_name == 'nav-home-security':
        template = 'tests/test-nav-home-security.html'
    else:
        raise Http404

    return index_render(request, template, {})

def index_render(request, template, context):
    context['page_name'] = 'index'
    context['pages'] = ['index']

    latest_news = Article.objects.order_by('-date_created')[:3]
    context['latest_news'] = latest_news
    try:
        tweets = cache.get('TWEETS')
        if tweets is None:
            t_api = twitter.Api()
            tweets = t_api.GetUserTimeline('@protectamerica')
            cache.set('TWEETS', tweets, 60*60)
        context['tweets'] = tweets[:3]
    except:
        context['tweets'] = []

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
    ctx['black_friday_delta'] = datetime(2012, 11, 23) - datetime(2012, 11, datetime.today().day)
    return simple_dtt(request, 'external/black-friday/index.html', ctx)