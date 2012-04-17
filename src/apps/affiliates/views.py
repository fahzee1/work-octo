from datetime import datetime, timedelta

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from apps.affiliates.models import Affiliate, LandingPage, AffTemplate
from apps.common.views import simple_dtt
from apps.contact.forms import PAContactForm
from apps.affiliates.forms import AddAffiliateForm

def post_to_old_pa(data):
    import httplib, urllib
    params = urllib.urlencode(data)
    headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"}
    conn = httplib.HTTPConnection("www.protectamerica.com:80")
    conn.request("POST", "/admin/scripts/edit_tracking.php", params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

def affiliate_view(request, affiliate, page_name=None):
    if page_name is None:
        page_name = 'index'
    try:
        affiliate = Affiliate.objects.get(agent_id=affiliate)
        request.session['refer'] = affiliate.name
        request.session['source'] = affiliate.name
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
def semlanding_response(request):
    expire_time = timedelta(days=90)

    forms = {}
    forms['basic'] = PAContactForm()
    response = render_to_response('affiliates/sem-landing-page/home.html',
                                  {'forms': forms},
                                  context_instance=RequestContext(request))
    
    return response

# used in the middleware to know what session to set
def semlanding_home(request):
    return semlanding_response(request)

def semlanding_google(request):
    return semlanding_response(request)

def semlanding_bing(request):
    return semlanding_response(request)


# custom admin view for adding affiliates
@staff_member_required
def add_affiliate(request):
    if request.method == 'POST':
        form = AddAffiliateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            aff_obj = form.save(commit=False)
            aff_obj.save()
            if data['landing_page']:
                # just set default coreg template
                coreg = AffTemplate.objects.get(folder='coreg')

                landingpage = LandingPage()
                landingpage.affiliate = aff_obj
                landingpage.template = coreg
                landingpage.save()
            pa_data = {
                'affil_id': aff_obj.agent_id,
                'name': aff_obj.name,
                'incentive': '',
                'email': '',
                'phone_number': aff_obj.phone,
                'pixel': aff_obj.pixels,
                'deposit': '199',
                'content': '',
                'add': True,
            }
            post_to_old_pa(pa_data)
            return HttpResponseRedirect('/django-admin/affiliates/affiliate/')
    else:
        form = AddAffiliateForm()
    return render_to_response('affiliates/add-affiliate.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))
