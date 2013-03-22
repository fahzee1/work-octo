from datetime import date, timedelta

from apps.common.views import get_active, simple_dtt
from apps.events.models import Event, Venue


def careers(request):
    events = Event.objects.all()
    yesterday = date.today()-timedelta(days=1)
    events = Event.objects.exclude(eventdate__lte=yesterday)[:2]

    return simple_dtt(request, 'contact-us/careers.html', {
                               'events': events,
                               'parent':'contact-us',
                               'pages': ['careers'],
                               'page_name': 'careers'})