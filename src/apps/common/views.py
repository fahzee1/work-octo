import re
from datetime import datetime, timedelta

from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from apps.contact.forms import PAContactForm, AffiliateLongForm

TESTING_PAGES = ['copper', 'bronze', 'silver', 'gold', 'platinum', 'copper-b', 'bronze-b', 'silver-b', 'gold-b', 'platinum-b']

def simple_dtt(request, template, extra_context):
    
    import urls
 
    def get_active(urllist, name, pages=None):
        if pages is None:
            pages = []
        for entry in urllist:
            try:
                pname = entry.default_args['extra_context']['page_name']
                if pname == name:
                    pages.append(pname)
                    return get_active(urllist, entry.default_args['extra_context']['parent'], pages)
            except:
                pass
        return pages

    #redirect to correct page if test
    package_test = request.COOKIES.get('package_test', None)
    if extra_context['page_name'] in TESTING_PAGES:
        # check to see if the page is a -b page
        B_PAGE = False;
        if re.search(r'-b', extra_context['page_name']):
            B_PAGE = True
        if package_test == 'a' and B_PAGE:
            return HttpResponseRedirect(reverse(
                extra_context['page_name'].split('-b')[0]))
        elif package_test == 'b' and not B_PAGE:
            return HttpResponseRedirect(reverse(
                '%s-b' % extra_context['page_name']))

    expire_time = timedelta(days=90)

    pages = get_active(urls.urlpatterns, extra_context['page_name'])
    forms = {}
    forms['basic'] = PAContactForm()
    forms['long'] = AffiliateLongForm()

    affiliate = request.COOKIES.get('refer_id', None)
    if not affiliate and 'agent_id' in extra_context:
        request.session['refer_id'] = extra_context['agent_id']

    response = render_to_response(template,
                              {'active_pages':pages,
                               'page_name':extra_context['page_name'],
                               'forms': forms},
                              context_instance=RequestContext(request))

    if 'agent_id' in extra_context and not affiliate:
        response.set_cookie('refer_id',
                        value=extra_context['agent_id'],
                        expires=datetime.now() + expire_time)
    if 'package_test' in extra_context and not package_test:
        response.set_cookie('package_test',
                        value=extra_context['package_test'],
                        expires=datetime.now() + expire_time)

    return response
