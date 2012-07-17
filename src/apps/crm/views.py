import urllib2
import feedparser
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from apps.crm.forms import LoginForm, AffiliateForm
from apps.affiliates.models import Affiliate, Profile

def crm_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', None)
            password = form.cleaned_data.get('password', None)

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('crm:index'))
    else:
        form = LoginForm()

    return render_to_response('crm/login.html', {
            'form': form,
        }, context_instance=RequestContext(request))

def index(request):

    # Display Latest Changes to the Website
    # rss -> https://github.com/batcave/protectamerica/commits/master.atom

    changes = feedparser.parse(
        'https://github.com/robrocker7/protectamerica/commits/master.atom?login=robrocker7&token=60952c2cdb279c500b7c8f14545e0531')
    change_list = []
    for entry in changes.entries[:10]:
        change = {
            'title': entry.title,
            'date': entry.updated,
            'author': entry.author,
            'author_pic': entry.media_thumbnail[0]['url'],
        }
        change_list.append(change)

    return render_to_response('crm/index.html', {
            'change_list': change_list,
        }, context_instance=RequestContext(request))

# affiliate pages

def affiliate_requests(request):

    request_list = Profile.objects.all()
    paginator = Paginator(request_list, 20)

    page = request.GET.get('page', '')
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        requests = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        requests = paginator.page(paginator.num_pages)

    return render_to_response('crm/requests.html', {
            'requests': requests,
        }, context_instance=RequestContext(request))

def affiliates(request):

    affiliate_list = Affiliate.objects.all()
    paginator = Paginator(affiliate_list, 20)

    page = request.GET.get('page', '')
    try:
        affiliates = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        affiliates = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        affiliates = paginator.page(paginator.num_pages)

    return render_to_response('crm/affiliates.html', {
            'affiliates': affiliates,
        }, context_instance=RequestContext(request))

def affiliates_edit(request, affiliate_id):

    try:
        affiliate = Affiliate.objects.get(id=affiliate_id)
    except:
        raise Http404

    if request.method == 'POST':
        form = AffiliateForm(request.POST, instance=affiliate)
        if form.is_valid():
            cdata = form.cleaned_data
            # we want to add a landing page object if the affiliate
            # doesn't have one already
            if not affiliate.has_landing_page():
                if cdata['has_landing_page']:
                    affiliate.add_landing_page()
            # if the checkbox is off check to see if we should remove the 
            # landing page object
            if not cdata['has_landing_page']:
                if affiliate.has_landing_page():
                    affiliate.remove_landing_page()
            form.save()
            messages.success(request,
                'You have successfully updated the affiliates information.')
            return HttpResponseRedirect(reverse('crm:affiliates_edit',
                kwargs={'affiliate_id': affiliate.id}))
        messages.error(request,
            'It seems that there was an error trying to update the affiliates information')
    else:
        form = AffiliateForm(instance=affiliate)

    return render_to_response('crm/affiliate_edit.html', {
            'form': form,
            'affiliate': affiliate,
        }, context_instance=RequestContext(request))