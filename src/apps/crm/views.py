import urllib2
import feedparser
import pdb
from datetime import datetime

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.comments.models import Comment
from django.utils import simplejson
from django.views.decorators.cache import never_cache

from apps.crm.forms import LoginForm, AffiliateForm, ProfileForm
from apps.affiliates.models import Affiliate, Profile
from apps.contact.models import CEOFeedback
from apps.testimonials.models import Textimonial
from django.db.models import Q

@never_cache
def json_response(x):
    return HttpResponse(simplejson.dumps(x, sort_keys=True, indent=2),
                        content_type='application/json; charset=UTF-8')




def count_gmail_cities(city,state):
    q1 = Q(city=city)| Q(city=city.lower())
    ceo_list = CEOFeedback.objects.filter(q1,state=state,feedback_type='positive')
    the_list = []
    for x in ceo_list:
        if '@gmail' or '@GMAIL' in x.email:
            the_list.append(x)
    return len(the_list)




def paginate_this(request,_list,num=20):
    paginator = Paginator(_list,num)
    page = request.GET.get('page','')
    try:
        new_list = paginator.page(page)
    except PageNotAnInteger:
        new_list = paginator.page(1)
    except EmptyPage:
        new_list = paginator.page(paginator.num_pages)
    return new_list

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

def crm_logout(request):
    logout(request)
    return redirect('crm:login')


@never_cache
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
    if request.user.groups.filter(name='TESTIMONIAL').count() == 1:
        # TEXTIMONIAL COUNTS
        textimonial_count = Textimonial.objects.all().count()
        unread_textimonial_count = Textimonial.objects.filter(date_read=None).count()
        displayed_textimonial_count = Textimonial.objects.filter(display=True).count()
        nondisplayed_textimonial_count = Textimonial.objects.filter(display=False).count()
        # CEO FEEDBACK COUNTS
        ceo_feedbacks = CEOFeedback.objects.all().count()
        unread_feedback_count = CEOFeedback.objects.filter(date_read=None).count()
        read_feedback_count = CEOFeedback.objects.filter(read=True).count()
        general_feeback_count = CEOFeedback.objects.filter(feedback_type='general',read=False,converted=False).count()
        positive_feedback_count = CEOFeedback.objects.filter(feedback_type='positive',read=False,converted=False).count()
        negative_feedback_count = CEOFeedback.objects.filter(feedback_type='negative',read=False,converted=False).count()
        other_count = CEOFeedback.objects.filter(feedback_type='other',read=False,converted=False).count()
        converted_count = CEOFeedback.objects.filter(converted=True).count()

        counts['textimonials'] = (unread_textimonial_count,
                                  displayed_textimonial_count,
                                  nondisplayed_textimonial_count,
                                  textimonial_count,
                                  ceo_feedbacks,
                                  unread_feedback_count,
                                  general_feeback_count,
                                  positive_feedback_count,
                                  negative_feedback_count,
                                  other_count,
                                  converted_count,
                                  read_feedback_count)

        newyork_count = count_gmail_cities('New York','NY')
        boston_count = count_gmail_cities('Boston','MA')
        la_count = count_gmail_cities('Los Angeles','CA')
        atl_count = count_gmail_cities('Atlanta','GA')
        chicago_count = count_gmail_cities('Chicago','IL')
        dallas_count = count_gmail_cities('Dallas','TX')
        detroit_count = count_gmail_cities('Detroit','MI')
        houston_count = count_gmail_cities('Houston','TX')
        miami_count = count_gmail_cities('Miami','FL')
        mn_count = count_gmail_cities('Minneapolis','MN')
        philly_count = count_gmail_cities('Philadelphia','PA')
        phoenix_count = count_gmail_cities('Phoenix','AZ')
        sj_count = count_gmail_cities('San Jose','CA')
        seattle_count = count_gmail_cities('Seattle','WA')
        washington_count = count_gmail_cities('Washington','DC')

        counts['cities'] = (newyork_count,
                            boston_count,
                            la_count,
                            atl_count,
                            chicago_count,
                            dallas_count,
                            detroit_count,
                            houston_count,
                            miami_count,
                            mn_count,
                            philly_count,
                            phoenix_count,
                            sj_count,
                            seattle_count,
                            washington_count)


    context['counts'] = counts

    return render_to_response(template, context,
        context_instance=RequestContext(request))

@login_required(login_url='/crm/login/')
def index(request):
    # Display Latest Changes to the Website
    # rss -> https://github.com/batcave/protectamerica/commits/master.atom
    changes = feedparser.parse(
        'https://github.com/fahzee1.private.atom?token=7f6e88eb75db13005ffd5c911cc6d834')
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
def affiliates_add(request):
    if request.method == 'POST':
        form = AffiliateForm(request.POST, prefix="affiliate")
        profileform = ProfileForm(request.POST, prefix="profile")
        if form.is_valid() and profileform.is_valid():
            cdata = form.cleaned_data
            affiliate = form.save(commit=False)
            affiliate.save()

            profile = profileform.save(commit=False)
            profile.affiliate = affiliate
            profile.save()

            messages.success(request,
                'You have successfully updated the affiliates information.')
            return HttpResponseRedirect(reverse('crm:affiliates_edit',
                kwargs={'affiliate_id': affiliate.id}))

        messages.error(request,
            'It seems that there was an error trying to update the affiliates information')
    else:
        form = AffiliateForm(prefix="affiliate")
        profileform = ProfileForm(prefix="profile")

    return crm_render_wrapper(request, 'crm/affiliate_edit.html', {
            'form': form,
            'profileform': profileform,
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
        profile = Profile()
        profile.affiliate = affiliate

    if request.method == 'POST':
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

@login_required(login_url='/crm/login/')
def textimonials(request):
    textimonial_list = Textimonial.objects.all().order_by('-date_created')
    paginator = Paginator(textimonial_list, 20)

    page = request.GET.get('page', '')
    try:
        textimonials = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        textimonials = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        textimonials = paginator.page(paginator.num_pages)

    return crm_render_wrapper(request, 'crm/textimonial_list.html', {
            'textimonials': textimonials,
        })

@login_required(login_url='/crm/login/')
def textimonials_unread(request):
    textimonial_list = Textimonial.objects.filter(date_read=None).order_by('-date_created')
    paginator = Paginator(textimonial_list, 20)

    page = request.GET.get('page', '')
    try:
        textimonials = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        textimonials = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        textimonials = paginator.page(paginator.num_pages)

    return crm_render_wrapper(request, 'crm/textimonial_list.html', {
            'textimonials': textimonials,
        })

@login_required(login_url='/crm/login/')
def textimonials_display(request):
    textimonial_list = Textimonial.objects.filter(display=True).order_by('-date_created')
    paginator = Paginator(textimonial_list, 20)

    page = request.GET.get('page', '')
    try:
        textimonials = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        textimonials = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        textimonials = paginator.page(paginator.num_pages)

    return crm_render_wrapper(request, 'crm/textimonial_list.html', {
            'textimonials': textimonials,
        })

@login_required(login_url='/crm/login/')
def textimonials_dont_display(request):
    textimonial_list = Textimonial.objects.filter(display=False).order_by('-date_created')
    paginator = Paginator(textimonial_list, 20)

    page = request.GET.get('page', '')
    try:
        textimonials = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        textimonials = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        textimonials = paginator.page(paginator.num_pages)

    return crm_render_wrapper(request, 'crm/textimonial_list.html', {
            'textimonials': textimonials,
        })

@login_required(login_url='/crm/login/')
def textimonial_view(request, textimonial_id):
    try:
        textimonial = Textimonial.objects.get(id=textimonial_id)
    except Textimonial.DoesNotExist:
        return json_response({'success': False, 'errors': ['no_textimonial']})

    textimonial.mark_as_read()
    textimonial.save()

    c = Context({'textimonial': textimonial})
    t = loader.get_template('crm/_partials/textimonial_ajax.html')
    return json_response({'success': True, 'html': t.render(c)})

@login_required(login_url='/crm/login/')
def textimonial_approve(request, textimonial_id):
    try:
        textimonial = Textimonial.objects.get(id=textimonial_id)
    except Textimonial.DoesNotExist:
        return json_response({'success': False, 'errors': ['no_textimonial']})

    textimonial.display = True
    textimonial.mark_as_read()
    textimonial.save()

    c = Context({'textimonial': textimonial})
    t = loader.get_template('crm/_partials/textimonial_approved_actions.html')
    return json_response({'success': True,
        'id': textimonial.id, 'html': t.render(c)})

@login_required(login_url='/crm/login/')
def textimonial_dont_display(request, textimonial_id):
    try:
        textimonial = Textimonial.objects.get(id=textimonial_id)
    except Textimonial.DoesNotExist:
        return json_response({'success': False, 'errors': ['no_textimonial']})

    textimonial.display = False
    textimonial.mark_as_read()
    textimonial.save()

    c = Context({'textimonial': textimonial})
    t = loader.get_template('crm/_partials/textimonial_nonapproved_actions.html')
    return json_response({'success': True,
        'id': textimonial.id, 'html': t.render(c)})

@login_required(login_url='/crm/login/')
def ceo_feedbacks(request):
    ceo_feedback_list = CEOFeedback.objects.order_by('-date_created')
    ceo_feedbacks = paginate_this(request,ceo_feedback_list)

    return crm_render_wrapper(request, 'crm/ceo_feedback_list.html', {
            'ceo_feedbacks': ceo_feedbacks,
        })

@login_required(login_url='/crm/login/')
def ceo_feedbacks_unread(request):
    ceo_feedback_list = CEOFeedback.objects.filter(date_read=None).order_by('-date_created')
    ceo_feedbacks = paginate_this(request,ceo_feedback_list)
    return crm_render_wrapper(request, 'crm/ceo_feedback_list.html', {
            'ceo_feedbacks': ceo_feedbacks,
        })

@login_required(login_url='/crm/login/')
def ceo_feedbacks_read(request):
    ceo_feedback_list = CEOFeedback.objects.filter(read=True).order_by('-date_created')
    ceo_feedbacks = paginate_this(request,ceo_feedback_list)
    return crm_render_wrapper(request, 'crm/ceo_feedback_list.html', {
            'ceo_feedbacks': ceo_feedbacks,
        })

@login_required(login_url='/crm/login/')
def ceo_feedbacks_general(request):
    ceo_feedback_list = CEOFeedback.objects.filter(feedback_type='general',read=False,converted=False).order_by('-date_created')
    ceo_feedbacks = paginate_this(request,ceo_feedback_list)
    ctx={'ceo_feedbacks':ceo_feedbacks}
    return crm_render_wrapper(request,'crm/ceo_feedback_list.html',ctx)

@login_required(login_url='/crm/login/')
def ceo_feedbacks_positive(request):
    ceo_feedback_list = CEOFeedback.objects.filter(feedback_type='positive',read=False,converted=False).order_by('-date_created')
    ceo_feedbacks = paginate_this(request,ceo_feedback_list)
    ctx={'ceo_feedbacks':ceo_feedbacks}
    return crm_render_wrapper(request,'crm/ceo_feedback_list.html',ctx)

@login_required(login_url='/crm/login/')
def ceo_feedbacks_negative(request):
    ceo_feedback_list = CEOFeedback.objects.filter(feedback_type='negative',read=False,converted=False).order_by('-date_created')
    ceo_feedbacks = paginate_this(request,ceo_feedback_list)
    ctx={'ceo_feedbacks':ceo_feedbacks}
    return crm_render_wrapper(request,'crm/ceo_feedback_list.html',ctx)

@login_required(login_url='/crm/login/')
def ceo_feedbacks_other(request):
    ceo_feedback_list = CEOFeedback.objects.filter(feedback_type='other',read=False,converted=False).order_by('-date_created')
    ceo_feedbacks = paginate_this(request,ceo_feedback_list)
    ctx={'ceo_feedbacks':ceo_feedbacks}
    return crm_render_wrapper(request,'crm/ceo_feedback_list.html',ctx)

@login_required(login_url='/crm/login/')
def ceo_feedbacks_posted(request):
    ceo_feedback_list = CEOFeedback.objects.filter(converted=True).order_by('-date_created')
    ceo_feedbacks = paginate_this(request,ceo_feedback_list)
    ctx={'ceo_feedbacks':ceo_feedbacks}
    return crm_render_wrapper(request,'crm/ceo_feedback_list.html',ctx)



@login_required(login_url='/crm/login/')
def feedback_view(request, feedback_id):
    try:
        feedback = CEOFeedback.objects.get(id=feedback_id)
    except CEOFeedback.DoesNotExist:
        return json_response({'success': False, 'errors': ['no_feedback']})

    feedback.mark_as_read()

    c = Context({'feedback': feedback})
    t = loader.get_template('crm/_partials/feedback_ajax.html')
    return json_response({'success': True, 'html': t.render(c)})

@login_required(login_url='/crm/login/')
def feedback_convert(request, feedback_id):
    try:
        feedback = CEOFeedback.objects.get(id=feedback_id)
    except CEOFeedback.DoesNotExist:
        return json_response({'success': False, 'errors': ['no_feedback']})

    feedback.mark_as_read()
    feedback.convert_to_textimonial()

    c = Context({'feedback': feedback})
    t = loader.get_template('crm/_partials/feedback_convert_actions.html')
    return json_response({'success': True,
        'id': feedback.id, 'html': t.render(c)})

def comment_posted(request):
    comment_id = request.GET.get('c', None)
    if not comment_id:
        return HttpResponseRedirect(reverse('crm:index'))
    comment = Comment.objects.get(id=comment_id)
    messages.success(request,
        'You have successfully submitted your comment.')
    return HttpResponseRedirect(reverse('crm:affiliates_edit',
        kwargs={'affiliate_id': comment.object_pk}))

def search(request):
    #pdb.set_trace()
    ctx = {}
    query = request.GET.get('q', None)
    came_from = request.META.get('HTTP_REFERER',None)
    if not came_from:
        came_from = 'crm:index'
    if not query:
        return redirect(came_from)
    q1 = Q(first_name__iexact=query)
    q2 = Q(last_name__iexact=query)
    q3 = Q(message__contains=query)
    textimonials=Textimonial.objects.filter(q1|q2|q3).order_by('-date_created')

    ctx['textimonials'] = textimonials
    ctx['query'] = query
    return crm_render_wrapper(request,'crm/search-results.html',ctx)

@login_required(login_url='/crm/login/')
def ceo_feedbacks_cities(request):
    city,state = request.GET['city'],request.GET['state']
    q1 = Q(city=city)| Q(city=city.lower())
    ceo_list = CEOFeedback.objects.filter(q1,state=state,feedback_type='positive')
    the_list = []
    for x in ceo_list:
        if '@gmail' or '@GMAIL' in x.email:
            the_list.append(x)

    ceo_feedbacks = paginate_this(request,the_list)
    ctx={'ceo_feedbacks':ceo_feedbacks}
    return crm_render_wrapper(request,'crm/ceo_feedback_list.html',ctx)








