import datetime
import pytz
from pytz import timezone

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.localflavor.us.us_states import US_STATES

from apps.contact.forms import PAContactForm
from apps.crimedatamodels.views import query_by_state_city
from apps.crimedatamodels.models import (State,
                                         CityLocation,
                                         ZipCode)

LOCAL_KEYWORDS = [
    'home-security-systems',
    'alarm-systems',
]
TIMEZONES = {
    'AL':'America/Chicago',
    'AK':'America/Anchorage',
    'AZ':'America/Phoenix',
    'AR':'America/Chicago',
    'CA':'America/Los_Angeles',
    'CO':'America/Denver',
    'CT':'America/New_York',
    'DE':'America/New_York',
    'DC':'America/New_York',
    'FL':'America/New_York',
    'GA':'America/New_York',
    'HI':'Pacific/Honolulu',
    'ID':'America/Denver',
    'IL':'America/Chicago',
    'IN':'America/Indianapolis',
    'IA':'America/Chicago',
    'KS':'America/Chicago',
    'KY':'America/New_York',
    'LA':'America/Chicago',
    'ME':'America/New_York',
    'MD':'America/New_York',
    'MA':'America/New_York',
    'MI':'America/New_York',
    'MN':'America/Chicago',
    'MS':'America/Chicago',
    'MO':'America/Chicago',
    'MT':'America/Denver',
    'NE':'America/Chicago',
    'NV':'America/Los_Angeles',
    'NH':'America/New_York',
    'NJ':'America/New_York',
    'NM':'America/Denver',
    'NY':'America/New_York',
    'NC':'America/New_York',
    'ND':'America/Chicago',
    'OH':'America/New_York',
    'OK':'America/Chicago',
    'OR':'America/Los_Angeles',
    'PA':'America/New_York',
    'RI':'America/New_York',
    'SC':'America/New_York',
    'SD':'America/Chicago',
    'TN':'America/Chicago',
    'TX':'America/Chicago',
    'UT':'America/Denver',
    'VT':'America/New_York',
    'VA':'America/New_York',
    'WA':'America/Los_Angeles',
    'WV':'America/New_York',
    'WI':'America/Chicago',
    'WY':'America/Denver',
}

def local_page_wrapper(request, keyword, city, state, zipcode):
    def get_state_code(statestr):
        for state in US_STATES:
            if statestr.lower() == state[1].lower():
                return state[0]
        return False
    statecode = get_state_code(state)
    if not statecode:
        raise Http404
    return local_page(request, statecode, city.capitalize())

def local_page(request, state, city):
    crime_stats_ctx = query_by_state_city(state, city)
    forms = {}
    forms['basic'] = PAContactForm()
    crime_stats_ctx['forms'] = forms
    tz = timezone(TIMEZONES[crime_stats_ctx['state']])
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

    crime_stats_ctx['background_time'] = background_time
    
    response = render_to_response('local-pages/index.html',
                              crime_stats_ctx,
                              context_instance=RequestContext(request))

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
    return render_to_response('local-pages/choose-state.html',
                              {'states': states,
                               'forms': forms,},
                              context_instance=RequestContext(request))

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
    return render_to_response('local-pages/choose-city.html',
                              {'cities': city_by_first_letter,
                               'forms': forms,
                               'state': state.abbreviation,},
                              context_instance=RequestContext(request))

def sitemap(request, keyword):
    pass