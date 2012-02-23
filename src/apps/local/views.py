import datetime
import pytz
from pytz import timezone

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.contact.forms import PAContactForm
from apps.crimedatamodels.views import query_by_state_city


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
    
    return render_to_response('local-pages/index.html',
                              crime_stats_ctx,
                              context_instance=RequestContext(request))
