import urllib2
import feedparser
from datetime import datetime

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.comments.models import Comment
from django.utils import simplejson

from apps.crm.forms import LoginForm, AffiliateForm, ProfileForm
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

def crm_render_wrapper(request, template, context):
    # get Affiliate counts
    counts = {}
    if request.user.groups.filter(name='AFFILIATE').count() == 1:
        my_aff_count = Affiliate.objects.filter(manager=request.user).count()
        total_aff_count = Affiliate.objects.all().count()
        total_pending = Profile.objects.filter(status='PENDING').count()
        total_declined = Profile.objects.filter(status='DECLINED').count()
        counts['affiliates'] = (my_aff_count, total_aff_count, total_pending,
            total_declined)

    context['counts'] = counts

    return render_to_response(template, context,
        context_instance=RequestContext(request))

@login_required(login_url='/crm/login/')
def index(request):

    # Display Latest Changes to the Website
    # rss -> https://github.com/batcave/protectamerica/commits/master.atom

    changes = feedparser.parse(
        'https://github.com/robrocker7/protectamerica/commits/master.atom?login=robrocker7&token=60952c2cdb279c500b7c8f14545e0531')
    change_list = []
    for entry in changes.entries[:10]:
        if 'Merge' in entry.title:
            continue
        change = {
            'title': entry.title,
            'date': datetime.strptime(entry.updated.split('T')[0], '%Y-%m-%d'),
            'author': entry.author,
            'author_pic': entry.media_thumbnail[0]['url'],
        }
        change_list.append(change)
    return crm_render_wrapper(request, 'crm/index.html', {
            'change_list': change_list,
        })

# affiliate pages
@login_required(login_url='/crm/login/')
def affiliate_requests(request):

    request_list = Profile.objects.all()
    pfilter = request.GET.get('filter', None)
    
    if pfilter == 'declined':
        request_list = request_list.filter(status='DECLINED')
    else:
        request_list = request_list.filter(status='PENDING')

    request_list = request_list.order_by('-date_created') 
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

    return crm_render_wrapper(request, 'crm/requests.html', {
            'requests': requests,
        })


@login_required(login_url='/crm/login/')
def affiliate_requests_decline(request, profile_id):
    try:
        profile = Profile.objects.get(id=profile_id)
    except:
        raise Http404

    if request.method == 'POST':
        message = request.POST.get('decline_message', None)
        profile.decline_affiliate(message)
        messages.success(request,
            'You have successfully declined the affiliate.')
    else:
        messages.error(request,
            'Seems you tried to request this decline without a post. >.<')
    return HttpResponseRedirect(reverse('crm:requests'))

@login_required(login_url='/crm/login/')
def affiliate_requests_edit(request, profile_id):

    try:
        profile = Profile.objects.get(id=profile_id)
    except:
        raise Http404

    if request.method == "POST":
        if 'profile' in request.GET:
            print 'profile'
            profileform = ProfileForm(request.POST, instance=profile,
                prefix="profile")
            form = AffiliateForm(prefix="affiliate") 
            if profileform.is_valid():
                profileform.save()
                messages.success(request,
                    'You have successfully updated the request information.')
                return HttpResponseRedirect(reverse('crm:affiliate_requests_edit',
                    kwargs={'profile_id': profile.id}))
        elif 'approved' in request.GET:
            print 'affiliate'
            profileform = ProfileForm(instance=profile,
                prefix="profile")
            form = AffiliateForm(request.POST, prefix="affiliate")
            if form.is_valid():
                affiliate = form.save(commit=False)
                new_aff = profile.accept_affiliate(affiliate.agent_id, affiliate.name,
                    affiliate.phone)
                new_aff.manager = request.user
                new_aff.save()
                messages.success(request,
                    'You have successfully approved your affiliate.')
                return HttpResponseRedirect(reverse('crm:affiliates_edit',
                    kwargs={'affiliate_id': new_aff.id}))
    else:
        profileform = ProfileForm(instance=profile, prefix="profile")
        form = AffiliateForm(prefix="affiliate")

    return crm_render_wrapper(request, 'crm/request_edit.html', {
            'form': form,
            'profileform': profileform,
            'profile': profile,
        })

@login_required(login_url='/crm/login/')
def affiliates(request):

    affiliate_list = Affiliate.objects.order_by('-date_created', 'agent_id')

    # create affiliate_list to use for typeahead
    typeahead = []
    for affiliate in affiliate_list:
        typeahead.append(affiliate.agent_id)

    typehead_src = simplejson.dumps(typeahead)
    mine = request.GET.get('all', None)
    if not mine:
        affiliate_list = affiliate_list.filter(manager=request.user)

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

    return crm_render_wrapper(request, 'crm/affiliates.html', {
            'affiliates': affiliates,
            'typeahead_src': typehead_src,
        })

@login_required(login_url='/crm/login/')
def affiliates_search(request):
    query = request.GET.get('q', None)
    if not query:
        messages.error(request,
            'The affiliate you searched for doesn\'t exist: query')
        return HttpResponseRedirect(reverse('crm:affiliates'))
    try:
        affiliate = Affiliate.objects.get(agent_id=query)
    except Affiliate.DoesNotExist:
        messages.error(request,
            'The affiliate you searched for doesn\'t exist: database')
        return HttpResponseRedirect(reverse('crm:affiliates'))
    return HttpResponseRedirect(reverse('crm:affiliates_edit',
        kwargs={'affiliate_id': affiliate.id}))

@login_required(login_url='/crm/login/')
def affiliates_delete(request, affiliate_id):
    try:
        affiliate = Affiliate.objects.get(id=affiliate_id)
    except:
        raise Http404

    messages.success(request,
        'You have successfully deleted affiliate: %s' % affiliate.agent_id)
    affiliate.delete()
    return HttpResponseRedirect(reverse('crm:affiliates'))

@login_required(login_url='/crm/login/')
def affiliates_edit(request, affiliate_id):

    try:
        affiliate = Affiliate.objects.get(id=affiliate_id)
    except Affiliate.DoesNotExist:
        raise Http404
    try:
        profile = Profile.objects.get(affiliate=affiliate)
    except Profile.DoesNotExist:
        profile = None


    if request.method == 'POST':
        if profile:
            form = AffiliateForm(request.POST, instance=affiliate,
                prefix="affiliate")
            profileform = ProfileForm(request.POST, instance=profile,
                prefix="profile")
            if form.is_valid() and profileform.is_valid():
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

                profileform.save()

                messages.success(request,
                    'You have successfully updated the affiliates information.')
                return HttpResponseRedirect(reverse('crm:affiliates_edit',
                    kwargs={'affiliate_id': affiliate.id}))
        else:
            form = AffiliateForm(request.POST, instance=affiliate,
                prefix="affiliate")
            profileform = ProfileForm(instance=profile,
                prefix="profile")
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
        form = AffiliateForm(instance=affiliate, prefix="affiliate")
        profileform = ProfileForm(instance=profile, prefix="profile")

    return crm_render_wrapper(request, 'crm/affiliate_edit.html', {
            'form': form,
            'affiliate': affiliate,
            'profileform': profileform,
            'profile': profile,
        })

def comment_posted(request):
    comment_id = request.GET.get('c', None)
    if not comment_id:
        return HttpResponseRedirect(reverse('crm:index'))
    comment = Comment.objects.get(id=comment_id)
    messages.success(request,
        'You have successfully submitted your comment.')
    return HttpResponseRedirect(reverse('crm:affiliates_edit',
        kwargs={'affiliate_id': comment.object_pk}))