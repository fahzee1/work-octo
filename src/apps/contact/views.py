import urls
import pdb
import requests
import logging
from datetime import datetime, timedelta
from string import Template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse,HttpResponseBadRequest
from django.template import RequestContext, loader, Context
from django.core.mail import send_mail, EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.conf import settings
from apps.contact.models import GoogleExperiment, Lead
from apps.contact.forms import (PAContactForm, ContactUsForm, OrderForm,
    CeoFeedbackForm, MovingKitForm, TellAFriendForm, DoNotCallForm, LeadForm, PayItForwardForm)
from apps.affiliates.models import Affiliate
from apps.common.views import get_active, simple_dtt
from django.template.loader import render_to_string
from xml.etree import ElementTree as ET



render_to_string = loader.render_to_string
TimeoutError = requests.exceptions.Timeout
from requests.exceptions import SSLError
logger = logging.getLogger('lead_conduit')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(settings.LC_LOG)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


def send_leadimport(data):
    from email import Charset
    Charset.add_charset('utf-8',Charset.SHORTEST,None,'utf-8')
    subject = '%s Lead Submission' % data['agent_id']
    t = loader.get_template('_partials/lead_submission_email.html')
    c = Context(data)
    send_mail(subject, t.render(c),
        'Protect America <noreply@protectamerica.com>',
        ['leadimport@protectamerica.com','cjogbuehi@protectamerica.com'], fail_silently=False)

    return True


def send_bizdev_email(data):
    subject = 'New Lead From Dealers Page!'
    message = 'Name : %s \n Email: %s \n Phone: %s' % (data['name'],data['email'],data['phone'])
    from_email = 'Protect America <noreply@protectamerica.com>'
    to_email = 'agent2.0@protectamerica.com'
    send_mail(subject,message,from_email,[to_email])


def send_conduit_error(data,title='LeadConduit Error',message=None,test=False,notify_all=True):
    if notify_all:
        contact_list = ['cjogbuehi@protectamerica.com','development@protectamerica.com','RYLAN@protectamerica.com']
    else:
        contact_list = ['cjogbuehi@protectamerica.com']
    if not test:
        if not message:
            message = "Error from lead conduit.\n The reason(s) are : %s \n The lead Id is %s \n The url is %s \n and the params sent to LC are %s" % (data['reasons'],data['lead_id'],data['url'],data['params'])
        from_email = 'Protect America <noreply@protectamerica.com>'
        send_mail(title,message,from_email,contact_list)



def post_to_leadconduit(data,test=False,retry=False):
    #pdb.set_trace()
    try:
        lead = Lead.objects.get(id=data['lead_id'])
    except Lead.DoesNotExist:
        lead = None

    # items lead conduit needs
    params = {'xxAccountId':settings.LEAD_ACCOUNT_ID,
              'xxCampaignId':settings.LEAD_CAMPAIGN_ID,
              'LEAD_ID':data['lead_id'],
              'xxTrustedFormCertUrl':data['trusted_url'],
              'Name':data['customername'],
              'Phone1':data['phone'],
              'email':data['email'],
              'Referrer_Page':data['formlocation'],
              'Agent_ID':data['agentid'],
              'Source':data['source'],
              'Affkey':data['affkey'],
              'Search_Keywords':data['searchkeywords'],
              'Search_Engine':data['searchengine'],
              'ip_address':data['ip'],
              'web_device':data['device']
                }
    if test:
        params.update({'xxTest':'true'})
    try:
        logger.info('Starting request to lead conduit... (lead id = %s)' % data['lead_id'])
        xml_request = requests.post('https://app.leadconduit.com/v2/PostLeadAction',params=params,timeout=10)
        if xml_request.status_code == 200:
            logger.info('Status code is %s.' % xml_request.status_code)
            reasons_list = []
            root = ET.fromstring(xml_request.content)
            response = root.find('result').text
            # get lead submission url from response
            try:
                url = root.find('url').text
            except:
                url = None
            # get lead submission id from response
            try:
                lead_id = root.find('leadId').text
            except:
                lead_id = None

            if lead:
                if retry:
                    if lead.number_of_retries > 20:
                        send_conduit_error(data,
                                           test=settings.LEAD_TESTING,
                                           title='Lead retries exceeded 20 attempts',
                                           notify_all=True,
                                           message= 'The lead below was set to rety = False. \n'
                                                    'Lead id : %s \n Name: %s \n Phone: %s \n Referrer Page: %s' % (data['lead_id'],
                                                                                                                   data['customername'],
                                                                                                                   data['phone'],
                                                                                                                   data['formlocation'])

                                            )

                        lead.retry = False
                        lead.lc_error = True
                        lead.save()
                        return

                    lead.number_of_retries += 1
                lead.lc_url = url
                lead.lc_id = lead_id

            logger.info('API response is %s' % response)
            if response == 'success':
                if lead:
                    lead.lc_error = False
                    lead.retry = False
                    lead.reason ='reason gone, successful retry'
                    lead.save()
            elif response == 'queued':
                if lead:
                    lead.lc_error = False
                    lead.retry = False
                    lead.reason ='reason gone, successful retry'
                    lead.save()
            elif response == 'failure':
                # if it fails loop through the reasons and save in db/email
                for x in root.findall('reason'):
                    reasons_list.append(x.text)
                if lead:
                    lead.lc_reason = str(reasons_list)
                    lead.lc_error = True
                    lead.retry = True
                    lead.save()
                data = {'reasons':reasons_list,
                        'lead_id':lead_id,
                        'url':url,
                        'params':params.items()}
                send_conduit_error(data,test=settings.LEAD_TESTING)
            elif  response == 'error':
                # if it fails loop through the reasons and save in db/email
                for x in root.findall('reason'):
                    reasons_list.append(x.text)
                if lead:
                    lead.lc_reason = str(reasons_list)
                    lead.lc_error = True
                    lead.retry = True
                    lead.save()
                data = {'reasons':reasons_list,
                        'lead_id':lead_id,
                        'url':url,
                        'params':params.items()}
                send_conduit_error(data,test=settings.LEAD_TESTING)

            try:
                if not data['agentid']:
                    send_conduit_error(data,test=settings.LEAD_TESTING,
                                            title='Lead missing Agent_ID',
                                            message=' Lead id : %s \n Name: %s \n Phone: %s \n Referrer Page: %s' % (data['lead_id'],
                                                                                                                    data['customername'],
                                                                                                                    data['phone'],
                                                                                                                    data['formlocation']),
                                            notify_all = True
                                            )
            except KeyError:
                pass


        elif xml_request.status_code == 502 or xml_request.status_code == 503 or xml_request.status_code == 504:
            #retry request, email lead, log to console
            logger.error('NO! Status Code is %s. Should retry request. Sending email to notify' % xml_request.status_code)
            if lead:
                lead.retry = True
                lead.save()
            send_conduit_error(data,test=settings.LEAD_TESTING)


        elif xml_request.status_code != 502 or xml_request.status_code != 503 or xml_request.status_code != 504 or xml_request.status_code != 200:
            logger.error('NO! Status Code is %s. Something bad happened notify activeprospect' % xml_request.status_code)
            # report to support@activeprospect.com
            msg = "Full url: %s\n Type: POST\n Http Status Code: %s\n Parameters: %s" %(xml_request.url,xml_request.status_code,params.items())
            from_email = 'Protect America <noreply@protectamerica.com>'
            send_mail('Bad Http Status Code',msg,from_email,['support@activeprospect.com','cjogbuehi@protectamerica.com'])
            if lead:
                lead.retry = True
                lead.save()

    except TimeoutError:
        logger.error('Leadconduit timed out! Send email to lead import, notify, and retry')
        if lead:
            lead.retry = True
            lead.save()
        send_conduit_error(data,title='Leadconduit Timeout',test=settings.LEAD_TESTING)

    except SSLError as sslerr:
        import traceback
        logger.error('SSL Error. Pretty common should be retried and go through soon.')
        logger.error('Traceback: {0}'.format(traceback.format_exc()))
        if lead:
            lead.retry = True
            lead.save()
        title='Leadconduit SSLError'
        message='SSLError. Dont worry will be fixed soon, {0}'.format(traceback.format_exc())
        send_conduit_error(data,title=title,message=message,test=settings.LEAD_TESTING)

    except Exception as e:
        #something else happened email everyone
        from traceback import format_exc
        logger.error('SHIT! something VERY unexpected happened. Notify everyone. Here is exception %s' % format_exc())
        if lead:
            lead.retry = True
            lead.save()
        title='Unknown Lead Conduit exception (lead id = %s)' % data['lead_id']
        message='%s' % format_exc()
        send_conduit_error(data,title=title,message=message,test=settings.LEAD_TESTING)



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


def send_thankyou(data):
    subject = 'Hello, Thank you for your interest!'
    t = loader.get_template('emails/thank_you.html')
    c = Context(data)
    msg = EmailMultiAlternatives(subject, t.render(c),
        'Protect America <noreply@protectamerica.com>', [data['email']])
    msg.attach_alternative(t.render(c), 'text/html')
    msg.send()

    return True

def send_ceoposiive(data):
    subject = 'Your Opinions Matter'
    from_email = 'Protect America <noreply@protectamerica.com>'
    to_email = data['email']
    html_content = render_to_string('emails/ceo_feedback_positive.html',data)
    try:
        msg = EmailMultiAlternatives(subject,html_content,from_email,[to_email])
        msg.attach_alternative(html_content,'text/html')
        msg.send()
    except:
        pass
    return True

def send_caroline_thankyou(request,data,agent):
    phone =settings.DEFAULT_PHONE
    if 'phone' in request.GET:
        data['pa_phone'] = request.GET['phone']
    elif agent is not None and agent.phone:
        data['pa_phone'] = agent.phone
    else:
        data['pa_phone'] = phone

    subject = 'Hello, Thank you for your interest!'
    from_email = 'Protect America <noreply@protectamerica.com>'
    to_email = data['email']
    html_content = render_to_string('emails/lead-email.html',data)
    msg = EmailMultiAlternatives(subject,html_content,from_email,[to_email])
    msg.attach_alternative(html_content,'text/html')
    msg.send()


def send_error(data):
    subject = 'Affiliate Not In Database'
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
    if not affkey and 'affkey' in request.GET:
        affkey = request.GET['affkey']

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

    # we want to put the google experiment id if there is no affkey
    google_id = request.COOKIES.get('utm_expid', None)
    if affkey is None and google_id is not None:
        test_b = request.COOKIES.get('has_set_test_b', False)
        try:
            googleexp = GoogleExperiment.objects.get(google_id=google_id)
            affkey = googleexp.name
            if test_b:
                affkey = affkey + ' B'
        except:
            pass

    return {
            'agent':agent,
            'agentid': agentid,
            'affkey': affkey,
            'source': source,
            'lead_id': lead_id,
            'agent': agent,
            'thank_you_url': thank_you_url,
        }

def device_type(request,device):
    #opm only wants to use cookie tracking on mobile
    if device == 'm':
        device = 'mobile'
        request.COOKIES['device'] = device
        request.session['device'] = device
    if device == 't':
        device = 'tablet'
    if device == 'd' or device == 'c':
        device = 'desktop'
    if not device:
        device = ''
    return device


def basic_post_login(request):
    # url for Trusted Form
    trusted_url = request.POST.get('trusted_form',None)
    f_values = request.POST.get('form_values',None)
    browser = request.META.get('HTTP_USER_AGENT',None)
    OS = request.POST.get('operating_system',None)
    device_letter = request.POST.get('device',None)
    device_name = device_type(request,device_letter)
    lead_data = {'trusted_url': trusted_url}
    acn_business_name = request.POST.get('business_name')
    if acn_business_name:
        request.POST = request.POST.copy()
        request.POST['name'] = '%s (%s)' % (acn_business_name,request.POST['name'])

    form = LeadForm(request.POST)
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
        formset.agent_id = request_data['agentid']
        formset.source = request_data['source']
        formset.affkey = request_data['affkey']

        searchkeywords = request.session.get('search_term', None)
        cikw = request.COOKIES.get('cikw', None)
        if searchkeywords is None and cikw is not None:
            searchkeywords = cikw

        formset.search_engine = request.session['search_engine']
        formset.search_keywords = searchkeywords
        formset.form_values = f_values
        formset.trusted_url = trusted_url
        formset.ip_address = request.META.get('REMOTE_ADDR',None)
        formset.retry = True
        formset.browser = browser
        formset.operating_system = OS
        formset.device = device_name
        if fdata['gclid']:
            formset.gclid = fdata['gclid']
        else:
            fdata['gclid'] = request.COOKIES.get('gclid',None)
            if fdata['gclid']:
                formset.gclid = fdata['gclid']
        formset.save()
        request_data['lead_id'] = formset.id
        '''
        lead_data.update(request_data)
        lead_data.update({'searchkeywords':searchkeywords,
                     'searchengine':request.session.get('search_engine',None),
                     'formlocation':formset.referer_page,
                     'ip':request.META.get('REMOTE_ADDR',None),
                     'customername':fdata['name'],
                     'phone':fdata['phone'],
                     'email':fdata['email'],
                     'device':device_name
                     })
        '''
        # notes field information
        package = request.POST.get('package', None)
        notes_list = []
        if package:
            notes_list.append('Package Requested: %s' % package)
        visited_pages = request.session.get('vpages', None)
        if visited_pages is not None:
            notes_list.append('Pages Visited: %s' % visited_pages)
        notes = '\n'.join(notes_list)
        notes = notes.replace('\'', '')
        emaildata = {
            'agent_id': request_data['agentid'],
            'source': request_data['source'],
            'customername': fdata['name'],
            'phone': fdata['phone'],
            'email': fdata['email'],
            'affkey': request_data['affkey'],
            'formlocation': formset.referer_page,
            'searchengine': request.session['search_engine'],
            'searchkeywords': searchkeywords,
            'lead_id': formset.id,
            'notes': notes
        }
        if acn_business_name:
            emaildata['customername'] = '%s (%s)' %(acn_business_name,fdata['name'])

        #post_to_leadconduit(lead_data,test=settings.LEAD_TESTING)
        #send_leadimport(emaildata)
        if not settings.LEAD_TESTING and fdata['email']:
            send_caroline_thankyou(request,emaildata,request_data['agent'])
        formset.thank_you_url = request_data['thank_you_url']
        return (formset, True)
    return (form, False)


@csrf_exempt
def ajax_post_unprotected(*args, **kwargs):
    return ajax_post(*args, **kwargs)

def ajax_post_protected(*args, **kwargs):
    return ajax_post(*args, **kwargs)


def ajax_post(request):
    if request.method != "POST":
        return HttpResponseRedirect('/')

    response_dict = {}
    form_type = request.POST['form']

    if form_type == 'dealers':
        send_bizdev_email(request.POST)
        return HttpResponse(simplejson.dumps({"success":True,'thank_you':'/thank-you'}))

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
    return HttpResponseBadRequest()




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
        if request.POST['rating'] == '4' or request.POST['rating'] == '5':
            data = {'customer': request.POST['name'],
                    'email': request.POST['email']}
            send_ceoposiive(data)


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



def order_form_ca(request):
    if request.method == "POST":
        formset, success = basic_post_login(request)
        if success:
            return HttpResponseRedirect('http://www.protectamericasecurity.ca%s' % formset.thank_you_url)
    else:
        formset = OrderForm()

        if 'package' in request.GET:
            formset.fields['package'].initial = request.GET['package']

    return simple_dtt(request, 'canada/order-package.html', {
                               'parent':'products',
                               'formset': formset,
                               'pages': ['products'],
                               'page_name': 'products'})

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
                               'page_name': 'do-not-call'})

def payitforward(request):
    if request.method == "POST":
        form = PayItForwardForm(request.POST)
        if form.is_valid():
            formset = form.save(commit=False)
            formset.save()
            formset.email_shawne()
            form.submitted = True

            return HttpResponseRedirect(reverse('payitforward-thankyou'))

    else:
        form = PayItForwardForm()

    return simple_dtt(request, 'payitforward/involved.html', {
                               'form': form,
                               'pages': ['about'],
                               'page_name': 'payitforward-involved'})


def ajax_log(request):
    if request.is_ajax():
        number = request.POST.get('number',None)
        link = request.POST.get('link',None)
        timestamp = datetime.now()
        if number and link:
            logger.info('Call measurement returned %s.\n Link:%s \n Timestamp:%s' % (number,link,timestamp))

        else:
            if link:
                logger.info('Call measurement didnt return number.\n Link:%s \n Timestamp:%s' % (link,timestamp))
            else:
                logger.info('Call measurement didnt return number.\n Timestamp:%s' % timestamp)
        return HttpResponse()
    return HttpResponseBadRequest()

