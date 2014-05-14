import urlparse
import cgi
import re
from datetime import datetime, timedelta

from django.conf import settings
import settings as temp_settings

from apps.affiliates.models import Affiliate

class AffiliateMiddleware(object):


    def process_view(self, request, view_func, view_args, view_kwargs):
        print 'process_view, %r' % request.get_full_path()
        print 'refer id was %r ' % request.session.get('refer_id')
        check_agent_request = request.GET.get('agent', None)
        if check_agent_request in settings.SUPER_AFFILIATES:
            try:
                affiliate = Affiliate.objects.get(agent_id=check_agent_request)
                request.session['refer_id'] = affiliate.agent_id
                request.session['source'] = affiliate.name
                request.session['phone_number'] = affiliate.phone
                request.session['call_measurement'] = False

            except Affiliate.DoesNotExist:
                request.session['refer_id'] = 'HOMESITE'
                request.session['source'] = 'PROTECT AMERICA'

        if 'agent' not in request.GET:
            if settings.SITE_ID == 3:
                viewname = view_func.__name__
                if viewname == 'semlanding_home':
                    request.session['refer_id'] = 'SEMDIRECT'
                elif viewname == 'semlanding_google':
                    request.session['refer_id'] = 'GOOGLEPPC'
                elif viewname == 'semlanding_bing':
                    request.session['refer_id'] = 'BINGPPC'
            if settings.SITE_ID == 4:
                request.session['refer_id'] = 'LocalSearch'

        from apps.common.context_processors import get_affiliate_from_request
        current_affiliate = get_affiliate_from_request(request)

        if request.GET.get('device') == 'm' and current_affiliate and current_affiliate.agent_id == 'GOOGLEPPC':
            googlemobile_affiliate = Affiliate.objects.get(agent_id='i10045')
            request.session['refer_id'] = 'i10045'
            request.session['affiliate'] = googlemobile_affiliate
            print 'refer id changed to %r ' % request.session.get('refer_id')
            print 'affiliate id changed to %r' % request.session.get('affiliate')
            return None


        refer = request.session.get('refer_id')
        cookie = request.COOKIES.get('refer_id')

        bing = False
        if refer == 'i10797':
            bing = True
        if refer == 'i10798':
            bing = True
        if refer == 'i10799':
            bing = True
        if refer == 'i10800':
            bing = True
        if refer == 'i10801':
            bing = True
        if refer == 'i10802':
            bing = True
        if refer == 'BINGPPC':
            bing = True
        if cookie == 'BINGPPC':
            bing = True
        if request.GET.get('agent') == 'BINGPPC':
            bing = True


        request.session['is_bing'] = bing

        print 'request session %s' % request.session['is_bing']


        print 'refer_id is now %r' % request.session.get('refer_id')
        return None

    def process_response(self, request, response):
        print 'process_response, %r' % request.get_full_path()
        print 'refer id was %r ' % request.session.get('refer_id')
        # first get the domain parts and information
        domain_parts = request.get_host().split('.')
        if (len(domain_parts) > 2):
            subdomain = domain_parts[0]
            if (subdomain.lower() == 'www'):
                subdomain = None
            domain = '.'.join(domain_parts[1:])
        else:
            subdomain = None
            domain = request.get_host()

        # try to get the port main for development
        try:
            domain, port = domain.split(':')
        except ValueError:
            port = None

        cookie_domain = '.%s' % domain
        # set the cookie_domain to the request object
        request.cookie_domain = cookie_domain

        request.session['domain'] = domain

        expire_time = timedelta(days=90)

        # get default agent id from settings

        try:
            default_agent = settings.DEFAULT_AGENT
        except AttributeError:
            default_agent = None

        try:
            default_source = settings.DEFAULT_SOURCE
        except AttributeError:
            default_source = 'PROTECT AMERICA'

        affiliate = None
        current_cookie = request.COOKIES.get('refer_id', None)
        current_source = request.COOKIES.get('source', None)
        check_agent_request = request.GET.get('agent', None)
        if check_agent_request in settings.SUPER_AFFILIATES:
            try:
                affiliate = Affiliate.objects.get(agent_id=check_agent_request)
                request.session['refer_id'] = affiliate.agent_id
                request.session['source'] = affiliate.name
                request.session['phone_number'] = affiliate.phone
                request.session['call_measurement'] = False
                current_cookie = None
                current_source = None
            except Affiliate.DoesNotExist:
                request.session['refer_id'] = 'HOMESITE'
                request.session['source'] = 'PROTECT AMERICA'

        elif current_cookie is None:
            refer_id = request.session.get('refer_id', None)
            if refer_id is not None:
                try:
                    affiliate = Affiliate.objects.get(agent_id=refer_id)
                    request.session['refer_id'] = affiliate.agent_id
                    request.session['source'] = affiliate.name

                except Affiliate.DoesNotExist:
                    request.session['refer_id'] = 'HOMESITE'
                    request.session['source'] = 'PROTECT AMERICA'

            elif 'agent' in request.GET:
                try:
                    affiliate = Affiliate.objects.get(agent_id=request.GET['agent'])
                    request.session['refer_id'] = affiliate.agent_id
                    request.session['source'] = affiliate.name
                except Affiliate.DoesNotExist:
                    request.session['refer_id'] = 'HOMESITE'
                    request.session['source'] = 'PROTECT AMERICA'

            else:
                if default_agent is not None and current_cookie is None:
                    # we are going to assume that because there is no
                    # default agent and that the current_cookie is None
                    # that the visitor is organic
                    request.session['refer_id'] = default_agent
                    request.session['source'] = default_source
                else:
                    request.session['refer_id'] = 'HOMESITE'
                    request.session['source'] = 'PROTECT AMERICA'





        # Allow overwriting of affkey cookie
        if request.GET.get('affkey', None):
            request.session['affkey'] = request.GET.get('affkey')
            request.COOKIES['affkey'] = request.GET.get('affkey')

        if 'source' in request.GET and not current_source:
            request.session['source'] = request.GET['source']

        # for lead testing, don't set cookie
        if 'leadid' in request.GET:
            request.session['leadid'] = request.GET['leadid']

        # set the cookies here
        if 'refer_id' in request.session and request.session['refer_id'] != '' and not current_cookie:
            response.set_cookie('refer_id',
                value=request.session['refer_id'],
                domain=cookie_domain,
                expires=datetime.now() + expire_time)
        if 'source' in request.session and request.session['source'] != '' and not current_source:
            response.set_cookie('source',
                value=request.session['source'],
                domain=cookie_domain,
                expires=datetime.now() + expire_time)
        if 'utm_expid' in request.GET:
            response.set_cookie('utm_expid',
                value=request.GET['utm_expid'],
                domain=cookie_domain,
                expires=datetime.now() + expire_time)
        if 'cikw' in request.GET:
            response.set_cookie('cikw',
                value=request.GET['cikw'],
                domain=cookie_domain,
                expires=datetime.now() + expire_time)


        refer = request.session.get('refer_id')
        cookie = request.COOKIES.get('refer_id')
        print 'refer is %r ' % refer


        return response

