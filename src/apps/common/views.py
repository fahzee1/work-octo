import re
from datetime import datetime, timedelta
from urllib import urlencode

from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to

from apps.contact.forms import PAContactForm, AffiliateLongForm

def redirect_wrapper(request, agent_id):
    get = request.GET.copy()
    get['agent'] = agent_id

    return HttpResponseRedirect('/?%s' % urlencode(get))

def thank_you(request, custom_url=None):
    c = {'page_name': 'thank-you', 'custom_url': custom_url}
    return simple_dtt(request, 'thank-you/index.html', c)

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

def payitforward(request):

    videos = []
    videos.append({
        'charity': 'Hosanna House',
        'team': 'MSU Team: Movement Advertising',
        'url': 'http://www.youtube.com/watch?v=z9VxKbxjNsU',
    })
    videos.append({
        'charity': 'Help A Willing Kid',
        'team': 'MSU Team: Top Hat Media',
        'url': 'http://vimeo.com/38477884',
    })
    videos.append({
        'charity': 'Beekman Therapeutic Riding Center',
        'team': 'MSU Team: Five Star Media',
        'url': 'http://www.youtube.com/watch?v=IyR82vQDAKA',
    })
    videos.append({
        'charity': 'For Better Independence',
        'team': 'MSU Team: Inifinite Solutions',
        'url': 'http://www.youtube.com/watch?v=lAGzVtBliCo',
    })
    videos.append({
        'charity': 'Pay It Forward Challenge',
        'team': 'Protect America',
        'url': 'http://www.youtube.com/watch?v=HFhmcJiIZtQ',
    })

    forms = {}
    forms['basic'] = PAContactForm()
    forms['long'] = AffiliateLongForm() 

    return render_to_response('payitforward.html',
        {
            'page_name': 'payitforward',
            'forms': forms,
            'videos': videos,
        }, context_instance=RequestContext(request))
