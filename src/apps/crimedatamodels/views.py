import urllib
import pdb
import requests
from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import simplejson
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.conf import settings

from django.contrib.localflavor.us.us_states import US_STATES

from apps.contact.forms import PAContactForm
from django.template.defaultfilters import slugify
from apps.crimedatamodels.models import (CrimesByCity,
                                         CityCrimeStats,
                                         State,
                                         CityLocation,
                                         ZipCode,
                                         CrimeContent,
                                         MatchAddressLocation)

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


def query_by_state_city(state, city, get_content=True,local=False):
    # validate city and state
    try:
        state = State.objects.get(abbreviation=state)
        city_id = None
        print "this is state %s" % state.abbreviation
    except State.DoesNotExist:
        print 'none'
        raise Http404
    try:
        print city
        if ' ' not in city:
            cities = CityLocation.objects.filter(state=state.abbreviation)
            city_here=False
            local=(True if local else False)
            for x in cities:
                if x.join_name(local) == city:
                    city_here=True
                    city=x
                    print "this is city and length was 1 %s" % city
            if not city_here:
                raise Http404
        else:
            city = city.replace('+', ' ').replace('-', ' ').split(' ')
            _city=None
            city_slug=None

            if len(city)==2:
                f,l=city[0],city[1]
                if len(str(f))==2:
                    city=f+'.'+' '+l
                    _city=f+' '+l
                    _city_=f+'-'+l
                else:
                    city_slug=f.lower()+'-'+l.lower()
            if len(city)==3:
                f,s,t=city[0].lower(),city[1].lower(),city[2].lower()
                a,b,c=city[0],city[1],city[2]
                city_slug=f+'-'+s+'-'+t
                city=f+' '+s+' '+t
            if len(city)==4:
                f,s,t,l=city[0].lower(),city[1].lower(),city[2].lower(),city[3].lower()
                city_slug=f+'-'+s+'-'+t+'-'+l
            if len(city)==5:
                f,s,t,a,l=city[0].lower(),city[1].lower(),city[2].lower(),city[3].lower(),city[4].lower()
                city_slug=f+'-'+s+'-'+t+'-'+a+'-'+l
            print "this is city blah blah %s" % city
            if city_slug:
                city=CityLocation.objects.get(city_name_slug=city_slug,state=state.abbreviation)
            elif _city:
                aa=Q(city_name__iexact=city)
                bb=Q(city_name__iexact=_city)
                cc=Q(city_name__iexact=_city_)
                city=CityLocation.objects.get(aa|bb|cc,state=state.abbreviation)
            else:
                city=CityLocation.objects.get(city_name__iexact=city,state=state.abbreviation)

        print "this is edited city %s" % city
        city_id = city.id
    except CityLocation.DoesNotExist:
        print 'none'
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

    if city_crime_objs:
        # get population type
        if crimesbycity.population <= 40000:
            pop_type = 'TOWN'
        elif crimesbycity.population > 40000 and crimesbycity.population <= 750000:
            pop_type = 'CITY'
        else:
            pop_type = 'METROPOLIS'
    else:
        pop_type = 'METROPOLIS'


     # Google Weather API
    weather_info = query_weather(city.latitude, city.longitude,
        city.city_name, state.abbreviation)

    context={'crime_stats': (crime_stats if crime_stats else None),
           'years': years[:3],
           'latest_year': (crime_stats[years[0]] if crime_stats else None),
           'latest_year_':(city_crime_objs[0] if city_crime_objs else None),
           'state': state.abbreviation,
           'state_long': state.name,
           'city': city.city_name,
           'lat': city.latitude,
           'long': city.longitude,
           'weather_info': weather_info,
           'pop_type': pop_type,
           'city_id': city_id}

    # get content
    if get_content and city_crime_objs and crime_stats:
        content = CrimeContent.objects.get(
            grade=crime_stats[years[0]]['stats'].average_grade,
            population_type=pop_type)
        context.update(content=content.render(city))


    try:
        #try to see if the local page has an address associated with it 
        location_match=MatchAddressLocation.objects.select_related().get(location=city)
        context.update(local_street=location_match.address.street_name,
                       local_city=location_match.address.city,
                       local_state=location_match.address.state,
                       local_zipcode=location_match.address.zip_code)
    except MatchAddressLocation.DoesNotExist:
        pass

    return context

def crime_stats(request, state, city):
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
    crime_stats_ctx = query_by_state_city(state, city)

    forms = {}
    forms['basic'] = PAContactForm()
    crime_stats_ctx['forms'] = forms

    return render(request,'crime-stats/crime-stats.html',crime_stats_ctx)


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

    return render(request,'crime-stats/choose-city.html',
                              {'cities': city_by_first_letter,
                               'forms': forms,
                               'state': state.abbreviation,})


def choose_state(request):
    states = State.objects.order_by('name')
    forms = {}
    forms['basic'] = PAContactForm()
    if not settings.DEBUG:
        try:
            ip=request.META['REMOTE_ADDR']
            r=requests.get('http://freegeoip.net/json/'+ip)
            resp=r.json()
            city=resp['city']
            state_abbr=resp['region_code']
            state_long=resp['region_name']
        except:
            city=None
            state_abbr=None
        if city and state_abbr and 'dont_auto_crime_stats' not in request.session:
            request.session['dont_auto_crime_stats']=True
            try:
                return HttpResponseRedirect(reverse('crime-rate:crime-stats',kwargs={'city':city,'state':state_abbr}))
            except:
                return render(request,'crime-stats/choose-state.html',{'states':states,'forms':forms})
    return render(request,'crime-stats/choose-state.html',
                              {'states': states,
                               'forms': forms})

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

    return render(request,'crime-stats/choose-state.html',ctx)



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
    forms = {}
    forms['basic'] = PAContactForm()
    return render_to_response(
        'external/freecrimestats/state-page.html',
        {'states': US_STATES, 'forms': forms}, context_instance=RequestContext(request))


def cities(request, state):
    """State-Specific City Listing View"""

    state_obj = State.objects.get(abbreviation=state.upper())
    city_data = CityLocation.objects.all() \
        .filter(state=state.upper()) \
        .order_by('city_name')

    # Sort cities into alphabetized buckets
    cities_alph = {}
    for cd in city_data:
        letter = cd.city_name[:1].upper()
        if not cities_alph.get(letter):
            cities_alph[letter] = []
        cities_alph[letter].append(cd)
    forms = {}
    forms['basic'] = PAContactForm()
    buckets = sorted(cities_alph.items(), key=lambda item: item[0])
    return render_to_response('external/freecrimestats/city-page.html', {
            'state': state_obj.abbreviation,
            'state_long': state_obj.name,
            'cities_alph': buckets,
            'forms': forms
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
    data = query_by_state_city(state, city, get_content=False,local=True)
    data['cs_years'] = [(year, data['crime_stats'][year]) for year in data['years']]

    forms = {}
    forms['basic'] = PAContactForm()
    data['forms'] = forms

    # Collect Context and Render Template
    return render(request,'external/freecrimestats/results.html',data)


def crime(request, state, city, crime):
    """City-Specific Crime View"""

    # Find correct Template file, 404 if we don't have an entry for it.
    template = CRIME_TEMPLATES.get(crime, None)
    if not template:
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
    # Return Template with results of query_by_state_city
    return render_to_response(template,
        query_by_state_city(state, city, False,True),
        context_instance=RequestContext(request))


def search(request):
    """Render a search results page based on the query string in the GET params"""
    # Extract Query Parameters
    
    q_str = request.GET.get('q', None)
    city_and_state = False
    city_or_state = False
    is_zipcode = False
    n_cities = None
    city_objs = None
    if ',' in q_str:
        q_params = q_str.split(',')
        _city,_state = q_params[0],q_params[1]
        _state = _state.upper()
        city_and_state = True
    elif '/' in q_str:
        q_params = q_str.split('/')
        _city,_state = q_params[0],q_params[1]
        _state = _state.upper()
        city_and_state = True
    elif q_str.isdigit():
        is_zipcode = True
        q_params = q_str
    else:
        q_params =  q_str.capitalize()
        _city,_state = None,None
        city_or_state = True

       
    # Get any State objects from params, and replace
    # full state name params with abbreviations
    if not is_zipcode:
        try:
            query_abbr = (_state if city_and_state else q_params.upper())
            query_name = (_state if city_and_state else q_params.capitalize())
            q_abbr,q_name = query_abbr.replace(' ',''), query_name.replace(' ','')
            q1,q2 =  Q(abbreviation__iexact=q_abbr), Q(name__iexact=q_abbr)
            q3,q4 =  Q(abbreviation__iexact=q_name), Q(name__iexact=q_name)
            state = State.objects.get(q1|q2|q3|q4)
            print 'states are %s' % state.name
        except State.DoesNotExist:
            state = False


        if state:
            ss = state.abbreviation.upper()
            all_cities = CityLocation.objects.filter(state=ss)
        else:
            ss,dd = Q(city_name_slug=slugify(q_params)) ,Q(state__iexact=q_params)
            all_cities = CityLocation.objects.filter(ss|dd)
        if all_cities:
            list_all_cities=True
            print 'all cities are %s' % all_cities


    if is_zipcode:
        zip_qs = ZipCode.objects.filter(zip=q_params)
        n_zips = zip_qs.count()

        print 'zip codes are %s' % (zip_qs)

    # If we only matched 1 zip result, show that page automatically
        if n_zips == 1:
            zipcode = zip_qs[0]
            city_slug = zipcode.city.lower().replace(' ', '-')
            return HttpResponseRedirect(
                reverse('home') + zipcode.state + '/' + city_slug)

    # Otherwise get more creative (WIP)
        city_objs, n_cities = [], 0
        if n_zips > 0:
            city_names = [zc.city for zc in zip_qs]
            city_objs = CityLocation.objects.filter(city_name__in=city_names).order_by('city_name')
            n_cities = city_objs.count()


        print 'cities are %s' % (city_objs)

    # If only 1 city found, redirect to it's results like before
        if n_cities == 1:
            city = city_objs[0]
            return HttpResponseRedirect(
                reverse('home') + city.state + '/' + city.slug_name)


    if city_and_state:
        try:
            city = all_cities.get(city_name_slug=slugify((_city if city_and_state else q_params)))
        except CityLocation.DoesNotExist:
            messages.info(request,'Sorry no city/state/zipcode matching your querys')
            return redirect('home')
        return redirect('local',city.state,city.slug_name)

    forms = {}
    forms['basic'] = PAContactForm()

    ctx={'num_cities': (n_cities if n_cities else None), 
         'cities': (city_objs if city_objs else None), 
         'forms': forms, 
         'search_query': q_str}

    if list_all_cities:
        ctx.update(all_cities=all_cities)

    # Render search-results page
    return render(request,'external/freecrimestats/search-results.html',ctx)


def state_sitemap(request):
    from django.contrib.sitemaps.views import sitemap
    from apps.crimedatamodels.sitemaps import FreeCrimeStatsStateSitemap
    return sitemap(request, {'keyword-sitemap-index' : FreeCrimeStatsStateSitemap()})

def city_sitemap(request, state):
    from django.contrib.sitemaps.views import sitemap
    from apps.crimedatamodels.sitemaps import FreeCrimeStatsCitySitemap
    return sitemap(request, {'keyword-sitemap-cities' : FreeCrimeStatsCitySitemap(state)})

def crime_sitemap(request, state, city):
    from django.contrib.sitemaps.views import sitemap
    from apps.crimedatamodels.sitemaps import FreeCrimeStatsCrimeSitemap
    return sitemap(request, {'keyword-sitemap-index' : FreeCrimeStatsCrimeSitemap(state, city)})
