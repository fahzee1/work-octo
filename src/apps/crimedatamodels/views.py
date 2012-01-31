from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext


from apps.contact.forms import PAContactForm
from apps.crimedatamodels.models import (CrimesByCity,
                                         CityCrimeStats,
                                         State,
                                         CityLocation)

def crime_stats(request, state, city):
    # validate city and state
    try:
        state = State.objects.get(abbreviation=state)
    except State.DoesNotExist:
        raise Http404
    try:
        city = CityLocation.objects.get(city_name=city,
            state=state.abbreviation)
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
    forms = {}
    forms['basic'] = PAContactForm()
    return render_to_response('crime-stats/crime-stats.html',
                              {'crime_stats': crime_stats,
                               'years': years[:3],
                               'latest_year': crime_stats[years[0]],
                               'state': state.abbreviation,
                               'city': city.city_name,
                               'lat': city.latitude,
                               'long': city.longitude,
                               'forms': forms},
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
    return render_to_response('crime-stats/choose-city.html',
                              {'cities': city_by_first_letter,
                               'forms': forms,
                               'state': state.abbreviation,},
                              context_instance=RequestContext(request))

def choose_state(request):
    states = State.objects.order_by('name')

    forms = {}
    forms['basic'] = PAContactForm()
    return render_to_response('crime-stats/choose-state.html',
                              {'states': states,
                               'forms': forms,},
                              context_instance=RequestContext(request))
