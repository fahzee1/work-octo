import pdb
from datetime import datetime,date
from django.conf import settings
import calendar
from mobile.sniffer.detect import detect_mobile_browser
from mobile.sniffer.utilities import get_user_agent
from apps.affiliates.models import Affiliate


def business_time(request):
    ctx={'business_time':False}
    if not hasattr(settings,'BUSINESS_HOURS'):
        return ctx
    today=datetime.today()
    try:
        start=datetime.strptime('%s-%s-%s %s' % (
            today.day,
            today.month,
            today.year,
            settings.BUSINESS_HOURS[today.weekday()]['start'],
            ), '%d-%m-%Y %H%M')
        end=datetime.strptime('%s-%s-%s %s' % (
            today.day,
            today.month,
            today.year,
            settings.BUSINESS_HOURS[today.weekday()]['end'],
            ), '%d-%m-%Y %H%M')
        now=datetime.now()
        if start <= now <= end:
            ctx['business_time']=True
        else:
            ctx['business_time']=False
        return ctx
    except:
        return ctx

def last_day_of_month(request):
    #get final date of each month
    _now=str(datetime.now())
    now=_now.replace('-',' ')
    year=int(now[:4])
    month=int(now[4:7])
    last_day=calendar.monthrange(year,month)[1]
    last_date=str(month)+'/'+str(last_day)+'/'+str(year)
    _date=datetime.strptime(last_date,'%m/%d/%Y')

    #get weekend
    wknd=datetime.now().isoweekday()
    is_weekend=True
    if wknd != 6 or 7:
        is_weekend=False

    ctx={'final_date':_date,
         'is_weekend':is_weekend}
    return ctx

def mobile_check(request):
    ua = get_user_agent(request)
    is_mobile = False
    if ua:
        # Apply reg
        if detect_mobile_browser(ua):
            # Redirect the visitor from a web site to a mobile site
            is_mobile = True
    return {'is_mobile':is_mobile} 


def get_affiliate_from_request(request):
    affiliate = request.COOKIES.get('refer_id', None)
    check_affiliate = request.GET.get('agent', None)
    if check_affiliate in settings.SUPER_AFFILIATES:
        affiliate = check_affiliate
        affiliate = Affiliate.objects.get(agent_id=affiliate)

    if not affiliate:
        # try pulling the affiliate from the session
        affiliate = request.session.get('refer_id', None)
    if not affiliate:
        # still if the affiliate isn't found pull it form the agent
        affiliate = request.GET.get('agent', None)
    try:
        affiliate = Affiliate.objects.get(agent_id=affiliate)
        return affiliate
    except Affiliate.DoesNotExist:
        pass
    return None


def phone_number(request):
    from django.conf import settings
    ctx = {'phone_number': settings.DEFAULT_PHONE,
            'use_call_measurement': False}
    # we want to set the phone number in the session to keep from hVaving 
    # more than 1 databasecall

    session_num = request.session.get('phone_number', None)
    session_call_measurement = request.session.get('call_measurement', None)
    check_affiliate = request.GET.get('agent', None)

    if session_num is not None and session_call_measurement is not None and session_num != '':
        ctx['phone_number'] = session_num
        ctx['use_call_measurement'] = session_call_measurement
        return ctx

    # the affiliate cookie is not available on the first request
    # because of the nature of http. what this does is first check
    # the cookie (for subsequent visits), and if that doesn't exist
    # then we know the user either just got a cookie set (the
    # `source` GET var is set), or they do not have a source
    # So, first we check the cookie. If it doesn't exist, we check
    # the GET var. If neither of those exist, there is no affiliate
    affiliate = get_affiliate_from_request(request)

    if affiliate:
        request.session['affiliate']=affiliate
        if 'phone' in request.GET:
            ctx['phone_number'] = request.GET['phone']
            request.session['phone_number'] = request.GET['phone']
        else:
            ctx['phone_number'] = affiliate.phone
            request.session['phone_number'] = affiliate.phone
        ctx['use_call_measurement'] = affiliate.use_call_measurement
        request.session['call_measurement'] = affiliate.use_call_measurement

    #ctx['use_call_measurement'] = True

    return ctx


def tracking_pixels(request):
    ctx={}
    try:
        affiliate=request.session['affiliate']
        ctx['pixels']=affiliate.pixels
    except KeyError:
        ctx['pixels']=None
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

def detect_agent_id(request):
    data = {}
    agent_id = request.session.get('refer_id',None)
    if not agent_id:
        agent_id = request.COOKIES.get('refer_id',None)
    if agent_id and agent_id[0] == 'b':
        data['b_agent'] = True
    
    return data 
