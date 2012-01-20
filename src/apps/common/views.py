import re
from datetime import datetime, timedelta

from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from apps.contact.forms import PAContactForm, AffiliateLongForm

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

    return response
