import urls
from datetime import datetime, timedelta
from string import Template

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils import simplejson
from django.conf import settings

from apps.contact.forms import (PAContactForm, ContactUsForm, OrderForm, 
    CeoFeedbackForm, MovingKitForm, TellAFriendForm, DoNotCallForm)
from apps.affiliates.models import Affiliate
from apps.common.views import get_active, simple_dtt
from django.template.loader import render_to_string

def post_to_old_pa(data):
    import httplib, urllib
    params = urllib.urlencode(data)
    headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"}
    conn = httplib.HTTPConnection("www.protectamerica.com:80")
    conn.request("POST", "/scripts/go_lead_ajax.php", params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()


def send_leadimport(data):
    subject = '%s Lead Submission' % data['agent_id']
    t = loader.get_template('_partials/lead_submission_email.html')
    c = Context(data)
    send_mail(subject, t.render(c),
        'Protect America <noreply@protectamerica.com>',
        ['leadimport@protectamerica.com'], fail_silently=False)

    return True

def send_thankyou(data):
    subject = 'Hello, Thank you for your interest!'
    t = loader.get_template('emails/thank_you.html')
    c = Context(data)
    msg = EmailMultiAlternatives(subject, t.render(c),
        'Protect America <noreply@protectamerica.com>', [data['email']])
    msg.attach_alternative(t.render(c), 'text/html')
    msg.send()

    return True

def send_error(data):
    subject = 'Lead Submission Error'
    t = loader.get_template('emails/lead_submission_error.html')
    c = Context(data)
    send_mail(subject, t.render(c),
        'Protect America <noreply@protectamerica.com>',
        ['robert@protectamerica.com'], fail_silently=False)

def prepare_data_from_request(request):
    thank_you_url = '/thank-you'
    agentid = request.COOKIES.get('refer_id', None)
    if agentid is None:
        agentid = request.session.get('refer_id', None)
    if not agentid and 'agent_id' in request.POST:
        agentid = request.POST['agent_id']

    affkey = request.COOKIES.get('affkey', None)
    if affkey is None:
        affkey = request.session.get('affkey', None)
    if not affkey and 'affkey' in request.POST:
        affkey = request.POST['affkey']

    source = request.COOKIES.get('source', None)
    if source is None:
        source = request.session.get('source', None)
    if not source and 'source' in request.POST:
        source = request.POST['source']
    
    lead_id = request.COOKIES.get('lead_id', None)
    if lead_id is None:
        lead_id = request.session.get('lead_id', None)
    
    # get the aff from the database
    try:
        agent = Affiliate.objects.get(agent_id=agentid)
    except Affiliate.DoesNotExist:
        agent = None

    # If there is an agent lets check some special handling
    if agent:

        if not source:
            source = agent.name

        if agent.thank_you:
            thank_you_url = thank_you_url + agent.thank_you

        # If the agent needs to be a homesite and the source
        # needs to be the agent ID we check to see if the
        # homesite_override is true
        if agent.homesite_override:
            source = agentid
            agentid = 'HOMESITE'

        # Special 5LINX catch
        if agent.agent_id == 'a01526':
            source = '5LINX'
    return {
            'agentid': agentid,
            'affkey': affkey,
            'source': source,
            'lead_id': lead_id,
            'agent': agent,
            'thank_you_url': thank_you_url,
        }

def basic_post_login(request):
    form = PAContactForm(request.POST)
    if form.is_valid():
        fdata = form.cleaned_data
        
        request_data = prepare_data_from_request(request)

        formset = form.save(commit=False)
        referer_page = None
        if 'referer_page' in request.POST:
            referer_page = request.POST['referer_page']
        if not referer_page and 'HTTP_REFERER' in request.META:
            referer_page = request.META['HTTP_REFERER']
        formset.referer_page = referer_page
        formset.save()
        
        if request_data['lead_id'] is None:
            request_data['lead_id'] = formset.id
        
        if request_data['agentid'] == 'HOMESITE' and request_data['source'] == '':
            # check if the refer page has agent in the url
            try:
                search = re.search(r'agent=([A-Za-z0-9\_-]+)',
                    formset.referer_page)
            except TypeError:
                search = None

            if search:
                agent = search.group(1)
                send_error({
                        'name': fdata['name'],
                        'phone': fdata['phone'],
                        'email': fdata['email'],
                        'agent': agent,
                        'page': formset.referer_page,
                    })

        emaildata = {
            'agent_id': request_data['agentid'],
            'source': request_data['source'],
            'customername': fdata['name'],
            'phone': fdata['phone'],
            'email': fdata['email'],
            'affkey': request_data['affkey'],
            'formlocation': formset.referer_page,
            'searchengine': request.search_referrer_engine,
            'searchkeywords': request.search_referrer_term,
            'lead_id': formset.id,
        }
        send_leadimport(emaildata)
        send_thankyou(emaildata)
        
        formset.thank_you_url = request_data['thank_you_url']
        return (formset, True)
    return (form, False)

def ajax_post(request):
    if request.method != "POST":
        return HttpResponseRedirect('/')

    response_dict = {}
    form_type = request.POST['form']

    if form_type == 'basic':
        form, success = basic_post_login(request)
        if success:
            response_dict.update({'success': True,
                'thank_you': form.thank_you_url,
                'lead_id': form.id})
        else:
            response_dict.update({'errors': form.errors})

    response = HttpResponse(simplejson.dumps(response_dict),
        mimetype='application/javascript')

    if 'success' in response_dict and response_dict['success']:
        expire_time = timedelta(days=90)
        response.set_cookie('lead_id', value=form.id,
            domain='.protectamerica.com',
            expires=datetime.now() + expire_time)
    
    return response


def post(request):
    
    if request.method == "POST":
        formset = PAContactForm(request.POST)
        if formset.is_valid():
            formset.save()

    else:
        return HttpResponseRedirect(reverse('contact-us'))


# This is the main contact us form page
def main(request):
    forms = {}
    forms['basic'] = PAContactForm()
    if request.method == "POST":
        formset = ContactUsForm(request.POST)
        if formset.is_valid():
            form = formset.save(commit=False)
            form.save()
            form.email_company()

            return HttpResponseRedirect(reverse('contact-thank-you'))
    else:
        formset = ContactUsForm()

    return simple_dtt(request, 'contact-us/index.html', {
                               'parent':'contact-us',
                               'formset': formset,
                               'forms': forms,
                               'pages': ['contact-us'],
                               'page_name': 'contact-us'}) 

# This is the send feedback to CEO form
def ceo(request):
    if request.method == "POST":
        formset = CeoFeedbackForm(request.POST)
        if formset.is_valid():
            form = formset.save(commit=False)
            form.save()
            form.email_company()

            return HttpResponseRedirect(reverse('ceo-thank-you'))
    else:
        formset = CeoFeedbackForm()

    return simple_dtt(request, 'contact-us/feedback-ceo.html', {
                               'parent':'contact-us',
                               'formset': formset,
                               'pages': ['contact-us'],
                               'page_name': 'feedback-ceo'})


# This is the view for the moving kit
def moving_kit(request):
    if request.method == "POST":
        formset = MovingKitForm(request.POST)
        if formset.is_valid():
            form = formset.save(commit=False)
            form.save()
            form.email_company()

            return HttpResponseRedirect(reverse('moving-kit-thank-you'))
    else:
        formset = MovingKitForm()

    return simple_dtt(request, 'support/moving-kit.html', {
                               'parent':'support',
                               'formset': formset,
                               'pages': ['support'],
                               'page_name': 'moving-kit'})

def find_us(request):
    pass

def tell_a_friend(request):
    if request.method == "POST":
        formset = TellAFriendForm(request.POST)
        if formset.is_valid():
            form = formset.save(commit=False)
            form.save()
            form.email_friend()

            return HttpResponseRedirect(reverse('contact-tell-friend'))

    else:
        formset = TellAFriendForm()

    return simple_dtt(request, 'about-us/tell-a-friend.html', {
                               'parent':'support',
                               'formset': formset,
                               'pages': ['about-us'],
                               'page_name': 'tell-a-friend'})

def order_form(request):
    if request.method == "POST":
        formset, success = basic_post_login(request)         
        if success:
            return HttpResponseRedirect('http://www.protectamerica.com%s' % formset.thank_you_url)
    else:
        formset = OrderForm()

    if 'package' in request.GET:
        formset.fields['package'].initial = request.GET['package']

    return simple_dtt(request, 'order/order-package.html', {
                               'parent':'packages',
                               'formset': formset,
                               'pages': ['contact-us'],
                               'page_name': 'moving-kit'})

def donotcall(request):
    if request.method == "POST":
        formset = DoNotCallForm(request.POST)
        if formset.is_valid():
            form = formset.save(commit=False)
            form.save()
            form.email_company()

            return HttpResponseRedirect(reverse('contact-thank-you'))

    else:
        formset = DoNotCallForm()

    return simple_dtt(request, 'help/do-not-call.html', {
                               'parent':'help',
                               'formset': formset,
                               'pages': ['support', 'help'],
                               'page_name': 'tell-a-friend'})