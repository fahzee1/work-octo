from datetime import datetime

from django.conf import settings

from mobile.sniffer.detect import detect_mobile_browser
from mobile.sniffer.utilities import get_user_agent


def mobile_check(request):
    ua = get_user_agent(request)
    is_mobile = False
    if ua:
        # Apply reg
        if detect_mobile_browser(ua):
            # Redirect the visitor from a web site to a mobile site
            is_mobile = True
    return {'is_mobile':is_mobile} 


def phone_number(request):
    from django.conf import settings
    ctx = {'phone_number': settings.DEFAULT_PHONE,
            'use_call_measurement': False}

    # the affiliate cookie is not available on the first request
    # because of the nature of http. what this does is first check
    # the cookie (for subsequent visits), and if that doesn't exist
    # then we know the user either just got a cookie set (the
    # `source` GET var is set), or they do not have a source
    # So, first we check the cookie. If it doesn't exist, we check
    # the GET var. If neither of those exist, there is no affiliate
    affiliate = request.COOKIES.get('refer_id', None)
    if not affiliate:
        # try pulling the affiliate from the session
        affiliate = request.session.get('refer_id', None)
    if not affiliate:
        # still if the affiliate isn't found pull it form the agent
        affiliate = request.GET.get('agent', None)

    if affiliate:
        from apps.affiliates.models import Affiliate
        try:
            affiliate = Affiliate.objects.get(agent_id=affiliate)
            ctx['phone_number'] = affiliate.phone
            ctx['use_call_measurement'] = affiliate.use_call_measurement
        except Affiliate.DoesNotExist:
            # just going to return the default context in this case
            pass

    return ctx


def business_hours(request):
    ctx = {'business_hours': ''}

    if not hasattr(settings, 'BUSINESS_HOURS'):
        return ctx
    today = datetime.today()
    day_table = [
        'mon',
        'tues',
        'wed',
        'thurs',
        'fri',
        'sat',
        'sun'
    ]

    day_format = {}
    # First group unique times
    for index, day in enumerate(settings.BUSINESS_HOURS):
        gstr = '%s%s' % (day['start'], day['end'])
        if gstr not in day_format:
            day_format[gstr] = []
        day_format[gstr].append(index)
        

    def itemgetter(*items):
        if len(items) == 1:
            item = items[0]
            def g(obj):
                return obj[item]
        else:
            def g(obj):
                return tuple(obj[item] for item in items)
        return g

    
    html = ''
    for key, value in sorted(day_format.iteritems(), key=itemgetter(1)):
        # get datetimes
        start = key[:4]
        end = key[4:]
        stime = datetime(today.year,
                         today.month,
                         today.day,
                         int(start[:2]),
                         int(start[2:])).strftime('%I:%M%p')
        etime = datetime(today.year,
                         today.month,
                         today.day,
                         int(end[:2]),
                         int(end[2:])).strftime('%I:%M%p')

        # start html                 
        element = '<li>'
        element = element + '%s' % (day_table[value[0]].capitalize())
        if len(value) > 1:
            element = element + ' - %s' % (day_table[value[-1]].capitalize())
        element = element + ': %s - %s' % (stime, etime)
        element = element + ' CT</li>'

        html = html + element
    ctx['business_hours'] = html
    return ctx
