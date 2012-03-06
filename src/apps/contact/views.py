from string import Template

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils import simplejson

from apps.contact.forms import (PAContactForm, BasicContactForm, OrderForm, 
    CeoFeedback)

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


def send_email(recipient):
    # send emails to submitter and to the dialer 

    send_mail('Email sent', 'Here is the message.', 
        'robert@protectamerica.com', [recipient], 
        fail_silently=False)

    return True;

def send_leadimport(data):
    subject = 'Hello, Thank you for your interest!'
    message = Template("[header]\n\n \
[data]\n \
agent_id=$agentid \
source=$source \
customername=$name \
phone1=$phone \
phone2= \
address1= \
city= \
state= \
zip= \
email=$email \
creditrating= \
affkey=$affkey \
homeowner= \
status=X \
formlocation=$formlocation \
searchengine= \
searchkeywords=")
    send_mail(subject, message.safe_substitute(data),
        'robert@protectamerica.com', ['robrocker7@gmail.com'], fail_silently=False)

    return True


def ajax_post(request):
    if request.method != "POST":
        return HttpResponseRedirect('/')

    response_dict = {}
    form_type = request.POST['form']

    if form_type == 'basic':
        form = PAContactForm(request.POST)
        if form.is_valid():
            fdata = form.cleaned_data
            agentid = request.COOKIES.get('refer_id', None)
            if agentid is None:
                agentid = request.session.get('refer_id', None)

            affkey = request.COOKIES.get('affkey', None)
            if affkey is None:
                affkey = request.session.get('affkey', None)

            source = request.COOKIES.get('source', None)
            if source is None:
                source = request.session.get('source', None)
            
            leadid = request.COOKIES.get('leadid', None)
            if leadid is None:
                leadid = request.session.get('leadid', None)

            # Special Handling for SEM Landing pages
            # All agent ids should be HOMESITE and the SOURCE
            # should become the agent ID

            if agentid in ['SEMDIRECT', 'BINGPPC', 'GOOGLEPPC']:
                source = agentid
                agentid = 'HOMESITE'

            # Special Handling for 5LYNX pages
            # All 5LYNX leads should have their source
            # changed to 5LYNX

            if agentid == 'a01526':
                source = '5LINX'

            # Special Handling for LocalSearch pages
            # Change localsearch to HOMESITE and make
            # the source LocalSearch

            if agentid == 'LocalSearch':
                source = agentid
                agentid = 'HOMESITE'

            padata = {'l_fname': fdata['name'],
                      'email_addr': fdata['email'],
                      'l_phone1': fdata['phone'],
                      'agentid': agentid,
                      'source': source,
                      'key3': affkey,
                      'leadid': leadid,
                      }
            post_to_old_pa(padata)
            formset = form.save(commit=False)

            if request.META['HTTP_REFERER'] is not None:
                formset.referer_page = request.META['HTTP_REFERER']
            
            formset.save()
            response_dict.update({'success': True})
        else:
            response_dict.update({'errors': form.errors})

    return HttpResponse(simplejson.dumps(response_dict),
        mimetype='application/javascript')


def post(request):
    
    if request.method == "POST":
        formset = PAContactForm(request.POST)
        if formset.is_valid():
            formset.save()

    else:
        return HttpResponseRedirect(reverse('contact-us'))


def main(request):
    if request.method == "POST":
        formset = BasicContactForm(request.POST)
        if formset.is_valid():
            formset.save()
            # send_email(formset.cleaned_data['email'])
    else:
        formset = BasicContactForm()

    return render_to_response('contact-us/index.html', 
                              {'parent':'contact-us',
                               'formset': formset}, 
                              context_instance=RequestContext(request))

def ceo(request):
    if request.method == "POST":
        formset = CeoFeedback(request.POST)
        if formset.is_valid():
            formset.save()
            # send_email(formset.cleaned_data['email'])
    else:
        formset = CeoFeedback()

    return render_to_response('contact-us/feedback-ceo.html',
                              {'parent':'contact-us',
                               'formset': formset},
                              context_instance=RequestContext(request))


def find_us(request):
    pass


def order_form(request):
    if request.method == "POST":
        formset = OrderForm(request.POST)
        if formset.is_valid():
            fdata = formset.cleaned_data
            agentid = request.COOKIES.get('refer_id', None)
            if agentid is None:
                agentid = request.session.get('refer_id', None)

            affkey = request.COOKIES.get('affkey', None)
            if affkey is None:
                affkey = request.session.get('affkey', None)

            source = request.COOKIES.get('source', None)
            if source is None:
                source = request.session.get('source', None)
            
            leadid = request.COOKIES.get('leadid', None)
            if leadid is None:
                leadid = request.session.get('leadid', None)

            # Special Handling for SEM Landing pages
            # All agent ids should be HOMESITE and the SOURCE
            # should become the agent ID

            if agentid in ['SEMDIRECT', 'BINGPPC', 'GOOGLEPPC']:
                source = agentid
                agentid = 'HOMESITE'

            # Special Handling for 5LYNX pages
            # All 5LYNX leads should have their source
            # changed to 5LYNX

            if agentid == 'a01526':
                source = '5LYNX'

            padata = {'l_fname': fdata['name'],
                      'email_addr': fdata['email'],
                      'l_phone1': fdata['phone'],
                      'agentid': agentid,
                      'source': source,
                      'key3': affkey,
                      'leadid': leadid,
                      }
            post_to_old_pa(padata)
            form = formset.save(commit=False)

            if request.META['HTTP_REFERER'] is not None:
                form.referer_page = request.META['HTTP_REFERER']
            
            form.save()
            # send_email(formset.cleaned_data['email'])
            return HttpResponseRedirect('http://www.protectamerica.com/pa/thank_you')
    else:
        formset = OrderForm()

    if 'package' in request.GET:
        formset.fields['package'].initial = request.GET['package']

    return render_to_response('order/order-package.html',
                              {'parent': 'packages',
                               'formset': formset},
                              context_instance=RequestContext(request))
