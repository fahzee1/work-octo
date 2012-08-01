import urlparse
import cgi
import re
from datetime import datetime, timedelta

from django.conf import settings
import settings as temp_settings

from apps.affiliates.models import Affiliate

class AffiliateMiddleware(object):

    
    def process_view(self, request, view_func, view_args, view_kwargs):
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

        return None

    def process_response(self, request, response):

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

        expire_time = timedelta(days=90)

        # get default agent id from settings

        try:
            default_agent = settings.DEFAULT_AGENT
        except AttributeError:
            default_agent = None

        affiliate = None
        current_cookie = request.COOKIES.get('refer_id', None)
        current_source = request.COOKIES.get('source', None)
        if not current_cookie:
            refer_id = request.session.get('refer_id', None)
            if refer_id is not None:
                try:
                    affiliate = Affiliate.objects.get(agent_id=refer_id)
                    request.session['refer_id'] = affiliate.agent_id
                    request.session['source'] = affiliate.name
                
                except Affiliate.DoesNotExist:
                    pass
                
            elif 'agent' in request.GET:
                try:
                    affiliate = Affiliate.objects.get(agent_id=request.GET['agent'])
                    request.session['refer_id'] = affiliate.agent_id
                    request.session['source'] = affiliate.name
                except Affiliate.DoesNotExist:
                    pass
                    
            else:
                if default_agent is not None and current_cookie is None:
                    # we are going to assume that because there is no
                    # default agent and that the current_cookie is None
                    # that the visitor is organic
                    request.session['refer_id'] = default_agent
                    request.session['source'] = 'PROTECT AMERICA'
                    
                    

        if 'affkey' in request.GET:
            request.session['affkey'] = request.GET['affkey']
            # Allow overwriting of affkey cookie

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

        
        return response

