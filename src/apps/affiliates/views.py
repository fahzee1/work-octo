from datetime import datetime, timedelta

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

from apps.affiliates.models import Affiliate, LandingPage, AffTemplate
from apps.common.views import simple_dtt
from apps.contact.forms import PAContactForm


def affiliate_view(request, affiliate, page_name=None):
    if page_name is None:
        page_name = 'index'
    try:
        affiliate = Affiliate.objects.get(agent_id=affiliate)
    except Affiliate.DoesNotExist:
        raise Http404

    landingpage = LandingPage.objects.get(affiliate=affiliate)
    htmlfilename = 'affiliates/%s/%s' % (landingpage.template.folder, landingpage.get_filename(page_name))

    return simple_dtt(request, htmlfilename, {'page_name': page_name,
        'agent_id': affiliate.agent_id})

def delta_sky(request):
    return affiliate_view(request, 'a03005')
    
def resources(request):
    return simple_dtt(request, 'affiliates/resources.html', {'page_name': 'affiliate_resources'})


# SEM Landing Page Views
def semlanding_response(request, agentid):
    expire_time = timedelta(days=90)

    forms = {}
    forms['basic'] = PAContactForm()
    response = render_to_response('affiliates/sem-landing-page/home.html',
                                  {'forms': forms},
                                  context_instance=RequestContext(request))
    
    current_cookie = request.COOKIES.get('refer_id', None)
    if not current_cookie:
        response.set_cookie('refer_id',
                            value=agentid,
                            expires=datetime.now() + expire_time)
    return response

def semlanding_home(request):
    return semlanding_response(request, 'SEM ORGANIC')

def semlanding_google(request):
    return semlanding_response(request, 'GOOGLE PPC')

def semlanding_bing(request):
    return semlanding_response(request, 'BING PPC')
