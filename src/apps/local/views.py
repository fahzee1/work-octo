import datetime
import pytz
from pytz import timezone
import settings
import os
import logging
import pdb

from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, render 
from django.template import RequestContext
from django.contrib.localflavor.us.us_states import US_STATES
from django.utils import simplejson
from django.conf import settings as dsettings
from django.views.decorators.cache import cache_page


from apps.contact.forms import PAContactForm
from apps.local.sitemaps import KeywordCitySitemap, KeywordStateSitemap, KeywordSitemapIndex
from apps.crimedatamodels.views import query_by_state_city
from apps.crimedatamodels.models import (State,
                                         CityLocation,
                                         ZipCode)


def get_timezone(state):
    tz = timezone(dsettings.TIMEZONES[state])
    utc_dc = datetime.datetime.now(tz=pytz.utc)
    new_dt = utc_dc.astimezone(tz)

    hour = int(new_dt.strftime("%H"))
    if hour >= 0 and hour < 6:
        background_time = 'night'
    elif hour >= 6 and hour < 8:
        background_time = 'dusk'
    elif hour >= 8 and hour < 18:
        background_time = 'day'
    elif hour >= 18 and hour < 20:
        background_time = 'dusk'
    elif hour >= 20 and hour < 24:
        background_time = 'night'
    return background_time


@cache_page(60 * 60 * 4)
def local_page_wrapper(request, keyword, city, state):
    if '-' in state:
        state=state.replace('-',' ').title()
    else:
        state=state.title()


    three=len(state.split(' '))
    if three==3:
        words=state.split(' ')
        first,second,third=words[0].capitalize(),words[1].lower(),words[2].capitalize()
        new_state=first+' '+second+' '+third

    statecode = None
    for x in US_STATES:
        if x[1] == (new_state if three == 3 else state) or x[0] == state.upper():
            statecode=x[0]   
        else:        
            for x in US_STATES:
                mult=x[1].split(' ')
                if len(mult) == 2:
                    first,second=mult[0].title(),mult[1].lower()
                    _state=first+second
                elif len(mult) == 3:
                    first,second,third=mult[0].title(),mult[1].lower(),mult[2].lower()
                    _state=first+second+third
                else:
                    _state=None
                if _state == state:
                    statecode=x[0]
    if not statecode:
        raise Http404

    if '-' and '.' in city:
        city=city.replace('-',' ').replace('.','')
    if '-' in city:
        city=city.replace('-',' ')
    if '.' in city:
        city=city.replace('.',' ')
    if '(' or ')' in city:
        city=city.replace('(','').replace(')','')
    if ',' in city:
        city=city.replace(',','')
    return local_page(request, statecode, city.title(), keyword)


def local_page(request, state, city, keyword=None):
    crime_stats_ctx = query_by_state_city(state, city)
    if crime_stats_ctx['city_id'] is not None and dsettings.SITE_ID == 4:
        json_file = os.path.join(settings.PROJECT_ROOT, 'src',
            'apps', 'crimedatamodels', 'external', 'city_state_redirect.json')
        json_data = open(json_file)
        csr = simplejson.load(json_data)
        zipcode = ZipCode.objects.filter(city=city, state=state)
        zipcodestr = '00000'
        if zipcode:
            zipcodestr = zipcode[0].zip
        state_obj = State.objects.get(abbreviation=state)
        return HttpResponsePermanentRedirect('http://www.protectamerica.com/%s/%s/%s/%s/' %
            (
                csr[str(crime_stats_ctx['city_id'])],
                city.lower().replace(' ', '-'),
                state_obj.name.lower().replace(' ', '-'),
                zipcodestr,
            ))

    forms = {}
    forms['basic'] = PAContactForm()
    crime_stats_ctx['forms'] = forms
    if keyword is not None:
        crime_stats_ctx['keyword'] = keyword.replace('-', ' ').title()

    background_time = get_timezone(crime_stats_ctx['state'])

    crime_stats_ctx['background_time'] = background_time

    if keyword in dsettings.CUSTOM_KEYWORD_LIST:
        response = render(request,'local-pages/%s.html', crime_stats_ctx) % keyword
    elif keyword in dsettings.WIRELESS_KEYWORD_LIST:
        response = render(request,'local-pages/wireless-home-security-systems.html',crime_stats_ctx)
    elif keyword in dsettings.ADT_KEYWORD_LIST:
        response = render(request,'landing-pages/adt.html',crime_stats_ctx)
    else:        
        response = render(request,'local-pages/index.html',crime_stats_ctx)

    expire_time = datetime.timedelta(days=90)
    response.set_cookie('affkey',
                    value='%s:%s' % (city.replace(' ', ''), state),
                    domain='.protectamerica.com',
                    expires=datetime.datetime.now() + expire_time)
    return response


def local_state(request):
    states = State.objects.order_by('name')

    forms = {}
    forms['basic'] = PAContactForm()
    return render_to_response('local-pages/choose-state.html', {
            'states': states, 'forms': forms
        }, context_instance=RequestContext(request))


def local_city(request, state):
    try:
        state = State.objects.get(abbreviation=state)
    except State.DoesNotExist:
        raise Http404

    cities = CityLocation.objects.filter(state=state.abbreviation)
    city_by_first_letter = {}
    for city in cities:
        if city.city_name[0] not in city_by_first_letter:
            city_by_first_letter[city.city_name[0]] = []
        city_by_first_letter[city.city_name[0]].append(city)
    forms = {}
    forms['basic'] = PAContactForm()
    return render_to_response('local-pages/choose-city.html', {
                'cities': city_by_first_letter,
                'forms': forms,
                'state': state.abbreviation,
            }, context_instance=RequestContext(request))


def html_sitemap(request, state, keyword):
    try:
        state = State.objects.get(abbreviation=state)
    except State.DoesNotExist:
        raise Http404

    cities = CityLocation.objects.filter(state=state.abbreviation)
    city_by_first_letter = {}
    for city in cities:
        if city.city_name[0] not in city_by_first_letter:
            city_by_first_letter[city.city_name[0]] = []
        city_by_first_letter[city.city_name[0]].append(city)
    forms = {}
    forms['basic'] = PAContactForm()
    return render_to_response('local-pages/html-sitemap.html', {
            'cities': city_by_first_letter,
            'forms': forms,
            'state': state.abbreviation,
            'keyword': keyword,
        }, context_instance=RequestContext(request))


def sitemap(request, keyword, state):
    from django.contrib.sitemaps.views import sitemap
    return sitemap(request, {'keyword-sitemap' : KeywordCitySitemap(keyword, state)})

def sitemap_state(request, keyword):
    from django.contrib.sitemaps.views import sitemap
    return sitemap(request, {'keyword-sitemap' : KeywordStateSitemap(keyword)})

def sitemap_index(request):
    from django.contrib.sitemaps.views import sitemap
    return sitemap(request, {'keyword-sitemap-index' : KeywordSitemapIndex(dsettings.LOCAL_KEYWORDS)})


