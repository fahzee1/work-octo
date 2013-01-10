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
from django.views.decorators.cache import cache_page, never_cache
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
    print('get_active:' + name)
    if pages is None:
        pages = []
    for entry in urllist:
        print('urlEntry:' + str(entry))
        #for test in dir(entry):
        #    print('test==' + test)
        #print('urlEntry:' + str(entry.name))

        print('===')
        try:
            pname = entry.default_args['extra_context']['page_name']
            if pname == name:
                pages.append(pname)
                return get_active(urllist, entry.default_args['extra_context']['parent'], pages)
        except:
            print('except')
            pass
    return pages

def simple_dtt(request, template, extra_context, expire_days=90):
    expire_time = timedelta(days=expire_days)

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

    if request.GET.get('affkey', None):
        request.session['affkey'] = request.GET.get('affkey')
        request.COOKIES['affkey'] = request.GET.get('affkey')


    if request.session.get('affkey'):
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

    #import json
    #json.dumps(extra_context)

    #for names in dir(extra_context):
        #print('names::' + names)

    #what is your goal here?
    # - ultimately to reolve the affkey issue
    # - in this case, trying to determine the context values 
    # - need to develop a caching solution for client and server
    # - need to be sure that nav is reflecting the current page selection 

    #for thekey in extra_context:
    #    print('key:: [' + thekey + ']:: ' + str(len(extra_context[thekey])) )
    #    if( len(extra_context[thekey]) > 0):
    #        print('subs of :^^^')
    #        for theSubKey in extra_context[thekey]:
    #            print('            ' + theSubKey + ':' )


    print('[[[affkey]]]: ' + extra_context['affkey'])
    print('[[[active_pages]]]: ' + str(len(extra_context['active_pages'])))


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
    elif test_name == 'holiday':
        template = 'tests/holiday-test.html'
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
    ctx['black_friday_delta'] = datetime(2013, 11, 22) - datetime(
        datetime.today().year, datetime.today().month, datetime.today().day)
    return simple_dtt(request, 'external/black-friday/index.html', ctx)

@never_cache
def five_linx(request, agent_id, page_name, parent):
    print('page_name: ' + page_name )

    tmplt = {}
    tmplt['home'] = 'affiliates/five-linx/index.html'
    tmplt['copper'] = 'affiliates/five-linx/copper.html'
    tmplt['makes-sense'] = 'affiliates/five-linx/makes-sense.html'
    tmplt['bronze'] = 'affiliates/five-linx/bronze.html'
    tmplt['silver'] = 'affiliates/five-linx/silver.html'
    tmplt['gold'] = 'affiliates/five-linx/gold.html'
    tmplt['platinum'] = 'affiliates/five-linx/platinum.html'
    tmplt['video'] = 'affiliates/five-linx/video.html'
    tmplt['gps'] = 'affiliates/five-linx/gps.html'
    tmplt['order'] = 'affiliates/five-linx/order.html'
    tmplt['thank-you'] = 'affiliates/five-linx/thank-you.html'


#dtt(r'^copper$', 'affiliates/five-linx/copper.html', 'copper', 'security-packages', ctx={
        #    'agent_id': 'a01526'}),
        #dtt(r'^makes-sense$', 'affiliates/five-linx/makes-sense.html', 'makes-sense', 'home', ctx={
        #    'agent_id': 'a01526'}),
        #dtt(r'^bronze$', 'affiliates/five-linx/bronze.html', 'bronze', 'security-packages', ctx={
        #    'agent_id': 'a01526'}),
        #dtt(r'^silver$', 'affiliates/five-linx/silver.html', 'silver', 'security-packages', ctx={
        #    'agent_id': 'a01526'}),
        #dtt(r'^gold$', 'affiliates/five-linx/gold.html', 'gold', 'security-packages', ctx={
        #    'agent_id': 'a01526'}),
        #dtt(r'^platinum$', 'affiliates/five-linx/platinum.html', 'platinum', 'security-packages', ctx={
        #    'agent_id': 'a01526'}),

        #dtt(r'^video$', 'affiliates/five-linx/video.html', 'video', ctx={
        #    'agent_id': 'a01526'}),

        #dtt(r'^gps$', 'affiliates/five-linx/gps.html', 'gps', ctx={
        #    'agent_id': 'a01526'}),
        
        #dtt(r'^order$', 'affiliates/five-linx/order.html', 'order', ctx={
        #    'agent_id': 'a01526'}),
            
        #dtt(r'^thank-you/5linx/$', 'affiliates/five-linx/thank-you.html', 'thank-you', ctx={
        #    'agent_id': 'a01526'}),

        #url(r'^dynamic/$', 'apps.common.views.black_friday', name='index'),


    ctx = {}
    ctx['page_name'] = page_name
    ctx['parent'] = parent

    #request.get('name')
    #if test_name == 'tcr-first':
    print('tmplt: ' + tmplt[page_name] )

    return simple_dtt(request, tmplt[page_name], extra_context=ctx)

