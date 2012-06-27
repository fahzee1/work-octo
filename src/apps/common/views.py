import re
import urls
from datetime import datetime, timedelta
from urllib import urlencode

from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to

from apps.contact.forms import PAContactForm, AffiliateLongForm, BasicContactForm
from apps.affiliates.models import Affiliate
from apps.common.forms import LinxContextForm
from apps.news.models import Article

def redirect_wrapper(request, agent_id):
    get = request.GET.copy()
    get['agent'] = agent_id

    return HttpResponseRedirect('/?%s' % urlencode(get))

def thank_you(request, custom_url=None):
    agent_id = request.COOKIES.get('refer_id', None)
    affiliate_obj = None
    try:
        affiliate_obj = Affiliate.objects.get(agent_id=agent_id)
    except Affiliate.DoesNotExist:
        pass

    # until the new lead system is ready go ahead and manually redirect
    # to new landing page here
    if affiliate_obj and affiliate_obj.thank_you and not custom_url:
        url = '/thank_you%s' % affiliate_obj.thank_you
        if 'leadid' in request.GET:
            url = url + '?leadid=%s' % request.GET['leadid']
        return HttpResponseRedirect(url)

    c = {'page_name': 'thank-you',
         'custom_url': custom_url,
         'affiliate_obj': affiliate_obj}
    return simple_dtt(request, 'thank-you/index.html', c)

def fivelinxcontest(request):
    if request.method == 'POST':
        form = LinxContextForm(request.POST)
        if form.is_valid():
            form.save() 
            return HttpResponseRedirect('/contest/thanks/')
    else:
        form = LinxContextForm()
    c = {'form': form,'page_name':'contest'}
    return simple_dtt(request, 'affiliates/five-linx/contest.html', c)

def fivelinxwinner(request):
    from apps.common.models import LinxContext
    winner = LinxContext.objects.order_by('?')
    return HttpResponse('%s' % winner[0])

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

def simple_dtt(request, template, extra_context):
    expire_time = timedelta(days=90)

    if 'pages' in extra_context:
        pages = extra_context['pages']
        pages.append(extra_context['page_name'])
    else:
        pages = get_active(urls.urlpatterns, extra_context['page_name'])

    forms = {}
    forms['basic'] = PAContactForm()
    forms['long'] = AffiliateLongForm()
    
    extra_context['forms'] = forms
    extra_context['active_pages'] = pages

    affiliate = request.COOKIES.get('refer_id', None)
    if not affiliate and 'agent_id' in extra_context:
        request.session['refer_id'] = extra_context['agent_id']

    response = render_to_response(template,
                              extra_context,
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

def index(request): 
    ctx = {}
    ctx['page_name'] = 'index'
    ctx['pages'] = ['index']

    latest_news = Article.objects.order_by('-date_created')[:3]
    ctx['latest_news'] = latest_news

    return simple_dtt(request, 'index.html', ctx)
