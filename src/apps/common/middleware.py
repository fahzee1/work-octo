# Ported by Matt Sullivan http://sullerton.com/2011/03/django-mobile-browser-detection-middleware/
import re
import urlparse
import cgi
import pdb

from django.utils.http import urlquote
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.conf import settings
from django.contrib.localflavor.us.us_states import US_STATES
from apps.local.views import get_statecode, strip_city
from django.shortcuts import redirect

reg_b = re.compile(r"android.+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|e\\-|e\\/|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\\-|2|g)|yas\\-|your|zeto|zte\\-", re.I|re.M)

class DetectMobileBrowser():
    def process_request(self, request):
        if settings.SITE_ID != 1 and settings.SITE_ID != 3:
            return None
        request.mobile = False
        current_cookie = request.session.get('redirect_mobile', None)
        check_agent = request.path
        if check_agent == '/getsmart':
            return None
        if 'no_mobile' in request.GET:
            current_cookie = True
            request.session['redirect_mobile'] = True

        if request.META.has_key('HTTP_USER_AGENT') and current_cookie is None:
            user_agent = request.META['HTTP_USER_AGENT']
            b = reg_b.search(user_agent)
            v = reg_v.search(user_agent[0:4])
            if b or v:
                return HttpResponseRedirect("http://m.protectamerica.com/")

class SearchEngineReferrerMiddleware(object):
    """
    This is exacly the same as snippet #197 http://www.djangosnippets.org/snippets/197/
    but returning search enigne, search engine domain and search term in:
    request.search_referrer_engine
    request.search_referrer_domain
    request.search_referrer_term

    Usage example:
    ==============
    Show ads only to visitors coming from a searh engine

    {% if request.search_referrer_engine %}
        html for ads...
    {% endif %}
    """
    SEARCH_PARAMS = {
        'AltaVista': 'q',
        'Ask': 'q',
        'Google': 'q',
        'Live': 'q',
        'Lycos': 'query',
        'MSN': 'q',
        'Yahoo': 'p',
        'Cuil': 'q',
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
                term = cgi.parse_qs(query).get(param)
                if term and term[0]:
                    term = ' '.join(term[0].split()).lower()
                    return (engine, network, term)
        return (None, network, None)


    def process_request(self, request):
        referrer = request.META.get('HTTP_REFERER')
        engine, domain, term = self.parse_search(referrer)
        request.session['search_engine'] = engine
        request.session['search_domain'] = domain
        request.session['search_term'] = term

class CommonMiddlewareWrapper(object):
    """
    Copying the code from django but wrapping it so that it will only fire
    if we are not in debug mode and the SITE_ID = 1
    """

    def process_request(self, request):
        """
        Check for denied User-Agents and rewrite the URL based on
        settings.APPEND_SLASH and settings.PREPEND_WWW
        """

        # Check for a redirect based on settings.APPEND_SLASH
        # and settings.PREPEND_WWW
        host = request.get_host()
        old_url = [host, request.path]
        new_url = old_url[:]

        if settings.SITE_ID != 1 or settings.DEBUG == True:
            return

        if (old_url[0] and not old_url[0].startswith('www.')):
            new_url[0] = 'www.' + old_url[0]

        if new_url == old_url:
            # No redirects required.
            return
        if new_url[0]:
            newurl = "%s://%s%s" % (
                request.is_secure() and 'https' or 'http',
                new_url[0], urlquote(new_url[1]))
        else:
            newurl = urlquote(new_url[1])
        if request.META.get('QUERY_STRING', ''):
            newurl += '?' + request.META['QUERY_STRING']
        return HttpResponsePermanentRedirect(newurl)



class MobilePageRedirect(object):
    def process_request(self,request):
        if settings.SITE_ID == 9:
            request.session['is_mobile'] = True
            url = request.path.rstrip('/').lstrip('/')

            match1 = re.compile(r'home-security-packages')
            match2 = re.compile(r'security-add-ons')
            match3 = re.compile(r'home-security-monitoring')
            match4 = re.compile(r'interactive-monitoring-features')
            match5 = re.compile(r'customer-info')
            match6 = re.compile(r'request-quote')
            match7 = re.compile(r'cart')

            if match1.match(url):
                return redirect('/home-security/')

            if match2.match(url):
                return redirect('/home-security-equipment/')

            if match3.match(url):
                return redirect('/learn-about-home-security/')

            if match4.match(url):
                return redirect('/learn-about-home-security/')

            if match5.match(url):
                return redirect('/contact-protect-america/')

            if match6.match(url):
                return redirect('/request-security-quote/')

            if match7.match(url):
                return redirect('/request-security-quote/')

        else:
            request.session['is_mobile'] = False
            return None







class LocalPageRedirect(object):
    """
    We dont want any local pages going to urls with full state names.
    ex home-security/TX/Austin instead of home-security/Texas/Austin.
    so check url and redirect if needed.
    """

    def process_request(self,request):
        #lets fist grab the url and check if its a local page
        url = request.path.rstrip('/').lstrip('/')

        #city page and state page
        match_cp = re.compile(r'home-security/[-\w]{3,}/[-\w]+')
        match_sp = re.compile(r'home-security/[-\w]{3,}')

        # redirect /rep/get-quote to homesecurity.protectamerica.com/rep/get-quote
        match_quote = re.compile(r'rep/get-quot')
        #match for new york - fix for rylan
        match_ny = re.compile(r'home-security/\bNY\b/[-\w]+',re.IGNORECASE)
        state_space = dict(US_STATES).values()
        state_nospace = [x.replace(' ','') for x in state_space]
        if match_quote.match(url):
            if request.META['HTTP_HOST'] != 'homesecurity.protectamerica.com':
                return redirect('http://homesecurity.protectamerica.com/rep/get-quot')

        if match_ny.match(url):
            #hardcoded redirect for NY
            ny = 'new-york-city'
            if ny in url or ny.title() in url or ny.capitalize() in url:
                return redirect('/home-security/NY/New-York')

        if match_cp.match(url):
            # city page so lets redirect
            chop_up = url.split('/')
            state, city = chop_up[1].replace('-',' '), strip_city(chop_up[2])
            for x in state_space:
                for y in state_nospace:
                    if x.upper() == state.upper() or y.upper() == state.upper():
                        statecode = get_statecode(state)
                        return redirect('/home-security/%s/%s' % (statecode,city.replace(' ','-').title()))

        elif match_sp.match(url):
            #state page so lets redirect
            chop_up = url.split('/')
            state = chop_up[1].replace('-',' ')
            for x in state_space:
                for y in state_nospace:
                    if x.upper() == state.upper() or y.upper() == state.upper():
                        statecode = get_statecode(state)
                        return redirect('/home-security/%s/' % (statecode))

        elif ' ' in url:
            url = re.sub("\s+","-",url)
            chop_up = url.split('/')
            if len(chop_up) == 3:
                return redirect('/' + chop_up[0].lower() + '/' + chop_up[1].upper() +'/' + chop_up[2].title())
            else:
                return None

        else:
            return None


