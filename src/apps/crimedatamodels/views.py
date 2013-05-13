import urllib

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import simplejson
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from django.contrib.localflavor.us.us_states import US_STATES

from apps.contact.forms import PAContactForm
from apps.crimedatamodels.models import CrimesByCity, CityCrimeStats, \
    State, CityLocation, ZipCode, CrimeContent


WEATHER_CODE_MAP = {
    '395': 'snow',
    '392': 'snow',
    '389': 'rain',
    '386': 'rain',
    '377': 'snow',
    '374': 'snow',
    '371': 'snow',
    '368': 'rain',
    '365': 'rain',
    '362': 'snow',
    '359': 'rain',
    '356': 'rain',
    '353': 'rain',
    '350': 'snow',
    '338': 'snow',
    '335': 'snow',
    '332': 'snow',
    '329': 'snow',
    '326': 'snow',
    '323': 'snow',
    '320': 'rain',
    '317': 'rain',
    '314': 'rain',
    '311': 'rain',
    '308': 'rain',
    '305': 'rain',
    '302': 'rain',
    '299': 'rain',
    '296': 'rain',
    '293': 'rain',
    '284': 'rain',
    '281': 'rain',
    '266': 'rain',
    '263': 'rain',
    '260': 'smoke',
    '248': 'smoke',
    '230': 'snow',
    '227': 'snow',
    '200': 'lightning',
    '185': 'rain',
    '182': 'rain',
    '179': 'rain',
    '176': 'rain',
    '143': 'smoke',
    '122': 'partly-cloudy',
    '119': 'cloudy',
    '116': 'partly-cloudy',
    '113': 'sunny',
}


def query_weather(latitude, longitude, city, state):
    # first try to get cache
    weather_info = cache.get('WEATHER:%s%s' % (city.lower().replace(' ', ''), state.lower()))
    if weather_info is None:
        try:
            url = 'http://free.worldweatheronline.com/feed/weather.ashx?q=%s,%s&format=json&num_of_days=2&key=1bed272811220539122102' % (latitude, longitude)
            result = simplejson.load(urllib.urlopen(url))
        except:
            return None
        if 'Error' in result:
            return None
        
        weather_info = {}
        condition = result['data']['current_condition'][0]

        weather_info['temp'] = condition['temp_F']
        weather_info['desc'] = condition['weatherDesc'][0]['value']
        weather_info['icon'] = WEATHER_CODE_MAP[condition['weatherCode']]

        cache.set('WEATHER:%s%s' %
            (city.lower().replace(' ', ''), state.lower()), weather_info, 60*60)
    return weather_info


def query_by_state_city(state, city, filters=None):
    # validate city and state
    try:
        state = State.objects.get(abbreviation=state)
        city_id = None
    except State.DoesNotExist:
        raise Http404
    try:
        city = city.replace('+', ' ').replace('-', ' ')
        city = CityLocation.objects.get(city_name__iexact=city,
            state=state.abbreviation)
        city_id = city.id
    except CityLocation.DoesNotExist:
        raise Http404

    city_crime_objs = CrimesByCity.objects.filter(
        fbi_city_name=city.city_name, fbi_state=state.abbreviation)

    crime_stats = {}
    years = []
    for crimesbycity in city_crime_objs:
        year = crimesbycity.year
        try:
            crime_stats[year] = {
                'stats': CityCrimeStats.objects.get(year=year,
                    city=crimesbycity),
                'info': crimesbycity}
        except CityCrimeStats.DoesNotExist:
            pass
        years.append(year)

    years.sort(reverse=True)

    # get population type
    if crimesbycity.population <= 40000:
        pop_type = 'TOWN'
    elif crimesbycity.population > 40000 and crimesbycity.population <= 750000:
        pop_type = 'CITY'
    else:
        pop_type = 'METROPOLIS'

    # get content
    content = CrimeContent.objects.get(
        grade=crime_stats[years[0]]['stats'].average_grade,
        population_type=pop_type)

    # Google Weather API
    weather_info = query_weather(city.latitude, city.longitude,
        city.city_name, state.abbreviation)
    
    return {'crime_stats': crime_stats,
           'years': years[:3],
           'latest_year': crime_stats[years[0]],
           'state': state.abbreviation,
           'state_long': state.name,
           'city': city.city_name,
           'lat': city.latitude,
           'long': city.longitude,
           'weather_info': weather_info,
           'pop_type': pop_type,
           'city_id': city_id,
           'content': content.render(city)}


def crime_stats(request, state, city):
    crime_stats_ctx = query_by_state_city(state, city)

    forms = {}
    forms['basic'] = PAContactForm()
    crime_stats_ctx['forms'] = forms
    return render_to_response('crime-stats/crime-stats.html',
                              crime_stats_ctx,
                              context_instance=RequestContext(request))


def choose_city(request, state):
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

    return render_to_response(
        'crime-stats/choose-city.html', {
            'cities': city_by_first_letter,
            'forms': forms,
            'state': state.abbreviation},
        context_instance=RequestContext(request))


def choose_state(request):
    if not settings.DEBUG:
        from django.contrib.gis.utils import GeoIP
        # try to auto find the city/state from IP address
        geo_ip = GeoIP()
        city_info = geo_ip.city(request.META['REMOTE_ADDR'])
        if city_info is not None and 'city' in city_info and 'region' in city_info and 'dont_auto_crime_stats' not in request.session:
            request.session['dont_auto_crime_stats'] = True
            return HttpResponseRedirect(reverse('crime-rate:crime-stats', kwargs={'city': city_info['city'], 'state': city_info['region']}))
    states = State.objects.order_by('name')

    forms = {}
    forms['basic'] = PAContactForm()
    return render_to_response(
        'crime-stats/choose-state.html', {
            'states': states,
            'forms': forms},
        context_instance=RequestContext(request))


def find_city(request):
    ctx = {}
    if 'q' in request.GET:
        try:
            # check to see if q is a int to assume a zipcode
            zipcode = int(request.GET['q'])
            # now check to see if the zip finds an ZipCode object
            try:
                zip_obj = ZipCode.objects.get(zip=zipcode)
                city_obj = CityLocation.objects.get(
                    city_name=zip_obj.city, state=zip_obj.state)
                return HttpResponseRedirect(city_obj.get_absolute_url())
            except ZipCode.DoesNotExist:
                ctx['error'] = 'zip_not_found'
        except:
            # assume its a string and try to find a city state match
            terms = request.GET['q'].split(',')
            terms = [term.strip() for term in terms]
            # check to see if terms[0] is a state
            try:
                state = State.objects.get(name=terms[0])
            except State.DoesNotExist:
                try:
                    state = State.objects.get(abbreviation__iexact=terms[0])
                except State.DoesNotExist:
                    state = None
            
            # if state is not "None" and terms is more than 1 try to
            # find a city otherwise redirect to the state page
            if state is not None and len(terms) > 1:
                try:
                    city_obj = CityLocation.objects.get(
                        state=state.abbreviation, city_name__iexact=terms[1])
                    return HttpResponseRedirect(city_obj.get_absolute_url())
                except CityLocation.DoesNotExist:
                    ctx['error'] = 'city_not_found'
            elif state is not None:
                return HttpResponseRedirect(
                    state.get_absolute_url() + '?q=%s' % request.GET['q'])

            # check to see if terms[0] is a city
            cities = CityLocation.objects.filter(city_name__iexact=terms[0])
            if len(cities) > 1 and len(terms) > 1:
                try:
                    state = State.objects.get(name=terms[1])
                except State.DoesNotExist:
                    try:
                        state = State.objects.get(abbreviation__iexact=terms[1])
                    except State.DoesNotExist:
                        state = None
                if state is not None:
                    cities = cities.get(state=state.abbreviation)
                    return HttpResponseRedirect(cities.get_absolute_url())
            
            # if cities == 1 then redirect
            if len(cities) == 1:
                return HttpResponseRedirect(cities[0].get_absolute_url())
            ctx['matches'] = cities

    forms = {}
    forms['basic'] = PAContactForm()
    ctx['forms'] = forms
    states = State.objects.order_by('name')
    ctx['states'] = states

    return render_to_response('crime-stats/choose-state.html',
        ctx, context_instance=RequestContext(request))


#
# Tim's FreeCrimeStats Views
#


# Map of passed 'Crime' strings, to their templates.
# (Makes it easy to change URLs without changing Template names.)
CRIME_TEMPLATES = {
    'burglary': 'external/freecrimestats/burglary.html',
    'robbery': 'external/freecrimestats/robbery.html',
    'motor-vehicle-theft': 'external/freecrimestats/motor-vehicle-theft.html',
    'violent-crime': 'external/freecrimestats/violent-crime.html',
    'larceny': 'external/freecrimestats/larceny.html'
}


def home(request):
    """Main Index View"""

    return render_to_response(
        'external/freecrimestats/index.html',
        {}, context_instance=RequestContext(request))


def states(request):
    """State Listing View"""

    return render_to_response(
        'external/freecrimestats/state-page.html',
        {'states': US_STATES}, context_instance=RequestContext(request))


def cities(request, state):
    """State-Specific City Listing View"""

    state_obj = State.objects.get(abbreviation=state.upper())
    city_data = CityLocation.objects.all() \
        .filter(state=state.upper()) \
        .order_by('city_name')

    return render_to_response('external/freecrimestats/city-page.html', {
            'state': state_obj.abbreviation,
            'state_long': state_obj.name,
            'cities': city_data
        }, context_instance=RequestContext(request))


def local(request, state, city):
    """City-Specific Index View"""

    # Collect filters from GET params
    filters = {
        'burglary': True,
        'robbery': True,
        'larceny': True,
        'vehicle': True,
        'violent': True}
    for filt in filters.keys():
        if request.GET.get(filt, None) == 'hide':
            filters[filt] = False

    # Collect Context and Render Template
    return render_to_response('external/freecrimestats/results.html',
        query_by_state_city(state, city),
        context_instance=RequestContext(request))


def crime(request, state, city, crime):
    """City-Specific Crime View"""

    # Find correct Template file, 404 if we don't have an entry for it.
    template = CRIME_TEMPLATES.get(crime, None)
    if not template:
        raise Http404

    # Return Template with results of query_by_state_city
    return render_to_response(template,
        query_by_state_city(state, city),
        context_instance=RequestContext(request))


def search(request):
    """Render a search results page based on the query string in the GET params"""

    # Extract Query Parameters
    q_str = request.GET.get('q', '')
    q_params = q_str.split('+')

    # Get potentially matching zips
    zqo = Q(zip__in=q_params) | Q(state__in=q_params)
    for qp in q_params:
        zqo = zqo | Q(city__contains=qp)
    zip_qs = ZipCode.objects.filter(zqo)
    n_zips = zip_qs.count()

    # If we only matched 1 zip result, show that page automatically
    if n_zips == 1:
        zipcode = zip_qs[0]
        city_slug = zipcode.city.lower().replace(' ', '-')
        return HttpResponseRedirect(
            reverse('home') + zipcode.state + '/' + city_slug)

    # Otherwise get more creative (WIP)
    city_objs = []
    if n_zips == 0:
        pass

    # Render search-results page
    return render_to_response('external/freecrimestats/search-results.html',
        {'num_cities': len(city_objs), 'cities': city_objs, 'search_query': q_str},
        context_instance=RequestContext(request))
