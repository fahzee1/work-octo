import re
import os
from datetime import datetime, timedelta
from django.shortcuts import render_to_response,render,redirect
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from apps.affiliates.models import Affiliate, LandingPage, AffTemplate,Profile
from apps.common.views import simple_dtt
from apps.contact.forms import PAContactForm
from apps.adspace.models import Ad, Campaign
from apps.affiliates.forms import AddAffiliateForm, AffiliateSignup, AffiliateLoginForm
import mimetypes
from django.contrib import messages



def json_response(x):
    return HttpResponse(simplejson.dumps(x, sort_keys=True, indent=2),
                        content_type='application/json; charset=UTF-8')

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
    landingpage = LandingPage.objects.filter(affiliate=affiliate)
    if landingpage:
        htmlfilename = 'affiliates/%s/%s' % (landingpage[0].template.folder, landingpage[0].get_filename(page_name))
    else:
        raise Http404

    return simple_dtt(request, htmlfilename, {'page_name': page_name,
        'agent_id': affiliate.agent_id})

def delta_view(request, affiliate, page_name=None):
    if page_name is None:
        page_name = 'index'
    try:
        affiliate = Affiliate.objects.get(agent_id=affiliate)
        request.session['refer'] = affiliate.name
        request.session['source'] = affiliate.name
    except Affiliate.DoesNotExist:
        raise Http404
    template = AffTemplate.objects.get(name=affiliate.name)
    landingpage = LandingPage.objects.get(affiliate=affiliate,template=template)
    htmlfilename = 'affiliates/%s/%s' % (landingpage.template.folder, landingpage.get_filename(page_name))

    return simple_dtt(request, htmlfilename, {'page_name': page_name,
        'agent_id': affiliate.agent_id})

def delta_sky(request):
    return delta_view(request, 'a03005')

def resources(request):
    """
    Function that gathers all the google ads from all the campaigns and
    then sends them to the html to be rendered by banner size.
    """
    aff_check=request.session.get('aff-logged-in',False)
    if not aff_check:
        print 'redirect'
        return redirect('affiliates:aff-login')


    campaigns = Campaign.objects.all()
    ads = {
        'leaderboard': ('Leaderboard (728x90)', []),
        'banner': ('Banner (468x60)', []),
        'skyscaper': ('Skyscraper (120x600)', []),
        'wide_skyscraper': ('Wide Skyscraper (160x600)', []),
        'small_square': ('Small Square (200x200)', []),
        'square': ('Square (250x250)', []),
        'medium_rectangle': ('Medium Rectangle (300x250)', []),
        'large_rectangle': ('Large Rectangle (336x280)', []),
    }
    for campaign in campaigns:
        for ad in campaign.ad_set.all():
            if ad.type.slug in ads:
                ads[ad.type.slug][1].append(ad)

    return simple_dtt(request, 'affiliates/resources/get-started.html', {
            'page_name': 'affiliate_resources',
            'google_ads': ads,
        })

def web_banners_page(request):
    """
    Function that gathers all the google ads from all the campaigns and
    then sends them to the html to be rendered by banner size.
    """
    campaigns = Campaign.objects.all()
    ads = {
        'leaderboard': ('Leaderboard (728x90)', []),
        'banner': ('Banner (468x60)', []),
        'skyscaper': ('Skyscraper (120x600)', []),
        'wide_skyscraper': ('Wide Skyscraper (160x600)', []),
        'small_square': ('Small Square (200x200)', []),
        'square': ('Square (250x250)', []),
        'medium_rectangle': ('Medium Rectangle (300x250)', []),
        'large_rectangle': ('Large Rectangle (336x280)', []),
    }
    for campaign in campaigns:
        for ad in campaign.ad_set.all():
            if ad.type.slug in ads:
                ads[ad.type.slug][1].append(ad)


    ctx={'page_name': 'aff-web-banners',
         'google_ads':ads,
          'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request, 'affiliates/resources/web-banners.html',ctx)

def agent_web_banners_page(request):
    """
    Function that gathers all the google ads from all the campaigns and
    then sends them to the html to be rendered by banner size.
    """
    campaigns = Campaign.objects.all()
    ads = {
        'leaderboard': ('Leaderboard (728x90)', []),
        'banner': ('Banner (468x60)', []),
        'skyscaper': ('Skyscraper (120x600)', []),
        'wide_skyscraper': ('Wide Skyscraper (160x600)', []),
        'small_square': ('Small Square (200x200)', []),
        'square': ('Square (250x250)', []),
        'medium_rectangle': ('Medium Rectangle (300x250)', []),
        'large_rectangle': ('Large Rectangle (336x280)', []),
    }
    for campaign in campaigns:
        for ad in campaign.ad_set.all():
            if ad.type.slug in ads:
                ads[ad.type.slug][1].append(ad)


    ctx={'page_name': 'aff-web-banners',
         'google_ads':ads,
          'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request, 'affiliates/resources/agents/web-banners.html',ctx)


def get_started_page(request):
    if not request.session.get('aff-logged-in',False):
        return redirect('aff-login')
    name_here=False
    if request.session.get('aff_name',False):
        name_here=True
        aff_name=request.session['aff_name']
    id_here=False
    if request.session.get('aff_id',False):
        id_here=True
        aff_id=request.session['aff_id']

    ctx={'page_name':'aff-get-started',
        'aff_name':(aff_name if name_here else None),
        'aff_id':(aff_id if id_here else None)}
    return simple_dtt(request,'affiliates/resources/get-started.html',ctx)



def logos_page(request):
    if not request.session.get('aff-logged-in',False):
        return redirect('aff-login')
    ctx={'page_name':'aff-logos',
         'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request,'affiliates/resources/logos.html',ctx)

def collateral_page(request):
    if not request.session.get('aff-logged-in',False):
        return redirect('aff-login')
    ctx={'page_name':'aff-collateral',
         'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request,'affiliates/resources/collateral.html',ctx)



def products_page(request):
    if not request.session.get('aff-logged-in',False):
        return redirect('aff-login')
    ctx={'page_name':'aff-products',
         'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request,'affiliates/resources/products.html',ctx)


def agent_page(request):
    if not request.session.get('aff-logged-in',False):
        return redirect('aff-login')
    ctx={'page_name':'agent-get-started',
         'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request,'affiliates/resources/agents/get-started.html',ctx)


def agent_web_banners_page(request):
    """
    Function that gathers all the google ads from all the campaigns and
    then sends them to the html to be rendered by banner size.
    """
    campaigns = Campaign.objects.all()
    ads = {
        'leaderboard': ('Leaderboard (728x90)', []),
        'banner': ('Banner (468x60)', []),
        'skyscaper': ('Skyscraper (120x600)', []),
        'wide_skyscraper': ('Wide Skyscraper (160x600)', []),
        'small_square': ('Small Square (200x200)', []),
        'square': ('Square (250x250)', []),
        'medium_rectangle': ('Medium Rectangle (300x250)', []),
        'large_rectangle': ('Large Rectangle (336x280)', []),
    }
    for campaign in campaigns:
        for ad in campaign.ad_set.all():
            if ad.type.slug in ads:
                ads[ad.type.slug][1].append(ad)


    ctx={'page_name': 'agent-web-banners',
         'google_ads':ads,
          'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request, 'affiliates/resources/agents/web-banners.html',ctx)


def agent_logos_page(request):
    if not request.session.get('aff-logged-in',False):
        return redirect('aff-login')
    ctx={'page_name':'agent-logos',
         'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request,'affiliates/resources/agents/logos.html',ctx)

def agent_support_page(request):
    if not request.session.get('aff-logged-in',False):
        return redirect('aff-login')
    ctx={'page_name':'agent-support',
         'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request,'affiliates/resources/agents/support.html',ctx)

def agent_collateral_page(request):
    if not request.session.get('aff-logged-in',False):
        return redirect('aff-login')
    ctx={'page_name':'agent-collateral',
         'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request,'affiliates/resources/agents/collateral.html',ctx)



def agent_products_page(request):
    if not request.session.get('aff-logged-in',False):
        return redirect('aff-login')
    ctx={'page_name':'agent-products',
         'aff_id':request.session.get('aff_id',None)}
    return simple_dtt(request,'affiliates/resources/agents/products.html',ctx)




# SEM Landing Page Views
def semlanding_response(request):
    expire_time = timedelta(days=90)

    forms = {}
    forms['basic'] = PAContactForm()
    response = render_to_response('affiliates/sem-landing-page/basic.html',
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
        form = AddAffiliateForm(request.POST, user=request.user)
        if form.is_valid():
            data = form.cleaned_data
            aff_obj = form.save(commit=False)
            if not request.user.is_superuser and not aff_obj.homesite_override:
                aff_obj.thank_you = '/affiliate/'
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
        form = AddAffiliateForm(user=request.user)
    return render_to_response('affiliates/add-affiliate.html',
        {'form': form},
        context_instance=RequestContext(request))

@staff_member_required
def edit_affiliate(request, affiliate_id):
    try:
        affiliate = Affiliate.objects.get(id=affiliate_id)
    except Affiliate.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = AddAffiliateForm(request.POST, instance=affiliate, user=request.user)
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
                'edit': True,
            }
            post_to_old_pa(pa_data)
            return HttpResponseRedirect('/django-admin/affiliates/affiliate/')
    else:
        form = AddAffiliateForm(instance=affiliate, user=request.user)

    return render_to_response('affiliates/add-affiliate.html',
        {'form': form, 'affiliate': affiliate},
        context_instance=RequestContext(request))

def request_agent_id(request):
    latest_agent = Affiliate.objects.latest('agent_id')

    def increment(agent_id):
        poped = []
        for char in agent_id:
            if char == 'a':
                poped.append(char)
                break
            if int(char) not in [1, 2, 3, 4, 5, 6, 7, 8 ,9]:
                poped.append(char)
            else:
                break
        agent_id = agent_id.replace(''.join(poped), '')
        agent_id = int(agent_id) + 1
        return '%s%s' % (''.join(poped), agent_id)

    new_id = increment(latest_agent.agent_id)

    # check for duplicate
    try:
        agent = Afffiliate.objects.get(agent_id=new_id)
    except:
        return json_response({'success': True, 'agent_id': new_id})
    return json_response({'success': False})

def signup(request):
    ctx = {}
    ctx['page_name'] = 'affiliate-program'
    ctx['pages'] = ['contact-us']

    if request.method == 'POST':
        form = AffiliateSignup(request.POST)
        if form.is_valid():
            aff = form.save(commit=False)
            aff.save()
            # send email to biz dev
            aff.send_signup_to_bizdev()
            aff.send_signup_email()
            return HttpResponseRedirect(reverse('affiliate-enroll'))
    else:
        form = AffiliateSignup()

    ctx['affform'] = form

    return simple_dtt(request, 'contact-us/affiliates.html', ctx)

@csrf_exempt
def accept_affiliate(request):
    # API listener to accept affiliate submissions
    if request.method != "POST":
        raise Http404

    errors = []

    # check to make sure all required information is available
    agent_id = request.POST.get('agentid', False).lower()
    name = request.POST.get('source', False)
    phone = request.POST.get('phone', '').replace('-', '')
    pixels = request.POST.get('tracking_pixels', '')
    conversion_pixels = request.POST.get('conversion_pixels', '')

    if not agent_id:
        errors.append('no_agentid_in_request')
    if not name:
        errors.append('no_source_in_request')

    try:
        affiliate = Affiliate.objects.get(agent_id=agent_id)
    except:
        affiliate = Affiliate()
        affiliate.agent_id = agent_id

    if len(errors):
        return json_response({'success': False, 'errors': errors})

    affiliate.name = name
    affiliate.phone = phone
    affiliate.pixels = pixels
    affiliate.conversion_pixels = conversion_pixels
    affiliate.thank_you = '/affiliate/'
    affiliate.save()

    return json_response({'success': True})

def get_affiliate_information(request, affiliate_id):

    try:
        affiliate = Affiliate.objects.get(agent_id=affiliate_id)
    except Affiliate.DoesNotExist:
        raise Http404

    info = {
        'source': affiliate.name,
        'phone': affiliate.phone,
        'tracking_pixels': affiliate.pixels,
        'conversion_pixels': affiliate.conversion_pixels,
    }

    return json_response({'success': True, 'affiliate': info})



def aff_login(request):
    form=AffiliateLoginForm()
    if request.method == 'POST':
        form=AffiliateLoginForm(request.POST)
        if form.is_valid():
            check_agentid = form.cleaned_data['agent_id']
            try:
                aff = Affiliate.objects.get(agent_id=check_agentid)
                if aff:
                    request.session['aff-logged-in']=True
                    request.session['aff_name']=aff.name
                    request.session['aff_id']=aff.agent_id

                    if check_agentid[0] == 'a' or check_agentid[0] == 'A':
                        response = redirect('aff-get-started')
                    elif (check_agentid[0] == 'b' or check_agentid[0] == 'B' or
                          check_agentid[0] == 'd' or check_agentid[0] == 'D'):
                        response = redirect('agent-get-started')
                    else:
                        response = redirect('aff-get-started')

                    response['Location'] +='?agent_id=%s' % aff.agent_id
                    return response

            except Affiliate.DoesNotExist:
                messages.info(request,'Please Enter The Correct Login.')
                return redirect('aff-login')
    else:
       form=AffiliateLoginForm()
    ctx={'form':form,'page_name':'aff-login'}
    return render(request,'affiliates/resources/login.html',ctx)







