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

from apps.crm.forms import LoginForm, AffiliateForm
from apps.affiliates.models import Affiliate

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
        'https://github.com/batcave/protectamerica/commits/master.atom?login=robrocker7&token=60952c2cdb279c500b7c8f14545e0531')
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
def affiliates(request):

    affiliate_list = Affiliate.objects.all()
    paginator = Paginator(affiliate_list, 25) # Show 25 contacts per page

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
    else:
        form = AffiliateForm(instance=affiliate)

    return render_to_response('crm/affiliate_edit.html', {
            'form': form,
            'affiliate': affiliate,
        }, context_instance=RequestContext(request))