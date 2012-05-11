import urlparse
import cgi
import re
from datetime import datetime, timedelta

from django.conf import settings
import settings as temp_settings

from apps.affiliates.models import Affiliate


class AffiliateMiddleware(object):
    # sniped the search engine code from this:
    # http://djangosnippets.org/snippets/197/

    SEARCH_PARAMS = {
        'AltaVista': 'q',
        'Ask': 'q',
        'Google': 'q',
        'Live': 'q',
        'Lycos': 'query',
        'MSN': 'q',
        'Yahoo': 'p',
    }
    
    NETWORK_RE = r"""^
        (?P<subdomain>[-.a-z\d]+\.)?
        (?P<engine>%s)
        (?P<top_level>(?:\.[a-z]{2,3}){1,2})
        (?P<port>:\d+)?
        $(?ix)"""
    
    @classmethod
    def parse_search(cls, url):
        """
        Extract the search engine, domain, and search term from `url`
        and return them as (engine, domain, term). For example,
        ('Google', 'www.google.co.uk', 'django framework'). Note that
        the search term will be converted to lowercase and have normalized
        spaces.

        The first tuple item will be None if the referrer is not a
        search engine.
        """
        try:
            parsed = urlparse.urlsplit(url)
            network = parsed[1]
            query = parsed[3]
        except (AttributeError, IndexError):
            return (None, None, None)
        for engine, param in cls.SEARCH_PARAMS.iteritems():
            match = re.match(cls.NETWORK_RE % engine, network)
            if match and match.group(2):
                term = cgi.parse_qs(unicode(query)).get(param)
                if term and term[0]:
                    term = u' '.join(term[0].split()).lower()
                    return (engine, network, term)
        return (None, network, None)
    
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

        expire_time = timedelta(days=90)

        # get default agent id from settings

        try:
            default_agent = settings.DEFAULT_AGENT
        except AttributeError:
            default_agent = None

        affiliate = None
        current_cookie = request.COOKIES.get('refer_id', None)
        if not current_cookie:
            refer_id = request.session.get('refer_id', None)
            if refer_id in ['GOOGLEPPC', 'BINGPPC', 'SEMDIRECT', 'LocalSearch']:

                response.set_cookie('refer_id',
                        value=request.session['refer_id'],
                        domain='.protectamerica.com',
                        expires=datetime.now() + expire_time)
            elif refer_id is not None:
                try:
                    affiliate = Affiliate.objects.get(agent_id=refer_id)
                    response.set_cookie('refer_id',
                        value=refer_id,
                        domain='.protectamerica.com',
                        expires=datetime.now() + expire_time)
                
                except Affiliate.DoesNotExist:
                    pass
                
            elif 'agent' in request.GET:
                try:
                    affiliate = Affiliate.objects.get(agent_id=request.GET['agent'])
                    request.session['refer_id'] = affiliate.agent_id
                    response.set_cookie('refer_id',
                        value=affiliate.agent_id,
                        domain='.protectamerica.com',
                        expires=datetime.now() + expire_time)
                except Affiliate.DoesNotExist:
                    pass
                    
            else:
                if default_agent is not None and current_cookie is None:
                    # dont set the cookie to default
                    request.session['refer_id'] = default_agent

                    response.set_cookie('refer_id',
                        value=request.session['refer_id'],
                        domain='.protectamerica.com',
                        expires=datetime.now() + expire_time)

        if 'affkey' in request.GET:
            request.session['affkey'] = request.GET['affkey']
            # Allow overwriting of affkey cookie
            response.set_cookie('affkey',
                value=request.GET['affkey'],
                expires=datetime.now() + expire_time)
        if 'source' in request.GET:
            request.session['source'] = request.GET['source']
            # Allow overwriting of affkey cookie
            response.set_cookie('source',
                value=request.GET['source'],
                expires=datetime.now() + expire_time)

        referrer = request.META.get('HTTP_REFERER')
        engine, domain, term = self.parse_search(referrer)
        if engine is not None:
            request.session['search_engine'] = engine
            request.session['search_keywords'] = term
        
        return response

