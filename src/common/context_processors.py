def is_business_time(request):
    from datetime import datetime
    BUSINESS_HOURS = [{   
            #monday
            'start': '0800',
            'end': '2100',
        },{
            #tuesday
            'start': '0800',
            'end': '2100',
        },{
            #wednesday
            'start': '0800',
            'end': '2100',
        },{
            #thursday
            'start': '0800',
            'end': '2100',
        },{
            #friday
            'start': '0800',
            'end': '2100',
        },{
            #saturday
            'start': '0800',
            'end': '1700',
        },]
    today = datetime.today()
    # day-month-year militarytime
    try:
        start = datetime.strptime('%s-%s-%s %s' % (
            today.day,
            today.month,
            today.year,
            BUSINESS_HOURS[today.weekday()]['start'],
            ), '%d-%m-%Y %H%M')
        end = datetime.strptime('%s-%s-%s %s' % (
            today.day,
            today.month,
            today.year,
            BUSINESS_HOURS[today.weekday()]['end'],
            ), '%d-%m-%Y %H%M')
        now = datetime.now()
        if start <= now <= end:
            return {'is_business_time': True}
        return {'is_business_time': False}
    except:
        return {'is_business_time': False}

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
    affiliate = request.COOKIES.get('affiliate', None)
    if not affiliate:
        # try pulling the affiliate from the ?source=
        affiliate = request.GET.get('source', None)

    if affiliate:
        from affiliates.models import Affiliate
        try:
            affiliate = Affiliate.objects.get(agent_id=affiliate)
            ctx['phone_number'] = affiliate.phone
            ctx['use_call_measurement'] = affiliate.use_call_measurement
        except Affiliate.DoesNotExist:
            # just going to return the default context in this case
            pass

    return ctx
