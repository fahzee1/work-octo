from itertools import chain

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, loader, Context
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.paginator import Paginator
from django.utils import simplejson
from django.core.urlresolvers import reverse

from apps.testimonials.models import Testimonial, Textimonial, Vidimonial
from apps.testimonials.forms import TestimonialForm, TextimonialForm
from apps.common.views import simple_dtt

def post_testimonial(request):
    # this view is to post a testimonial to the website
    # this will be used until the new testimonial pages are ready
    # The purpose of this is to submit the new testimonials to both the
    # old system and the new system so that when the change is made
    # we do not miss any testimonials
    if request.method == 'POST':
        # the post must have 'first_name', 
        # 'city', 'state', 'testimonial' in the submission
        testimonial = TestimonialForm(request.POST)
        if testimonial.is_valid():
            testimonial.save()
    else:
        raise Http404

def send_testimonial(request):
    if request.method == "POST":
        formset = TextimonialForm(request.POST)
        if formset.is_valid():
            form = formset.save(commit=False)
            form.save()
            form.email_company()

            return HttpResponseRedirect(reverse('contact-thank-you'))
            # send_email(formset.cleaned_data['email'])
    else:
        formset = TextimonialForm()

    return simple_dtt(request, 'about-us/send-testimonial.html', {
                               'parent':'about-us',
                               'formset': formset,
                               'pages': ['about-us', 'testimonials'],
                               'page_name': 'send-testimonial'})

def view_testimonials(request):
    testimonials = Textimonial.objects.filter(display=True).order_by('-date_created')
    vidimonials = Vidimonial.objects.order_by('-date_created')
    test_count = testimonials.count() + vidimonials.count()
    result_list = sorted(
        chain(testimonials, vidimonials),
        key=lambda instance: instance.date_created, reverse=True)

    paginator = Paginator(result_list, 20)
    page_num = request.GET.get('page', 1)
    page = paginator.page(page_num)

    left = []
    middle = []
    right = []
    loop_counter = 0
    
    for testimonial in page.object_list:
        if loop_counter == 0:
            left.append({'type': testimonial.__class__.__name__, 'obj': testimonial})
        elif loop_counter == 1:
            middle.append({'type': testimonial.__class__.__name__, 'obj': testimonial})
        elif loop_counter == 2:
            right.append({'type': testimonial.__class__.__name__, 'obj': testimonial})

        if loop_counter == 2:
            loop_counter = 0
        else:
            loop_counter = loop_counter + 1
    
    return simple_dtt(request, 'about-us/testimonials.html', {
                               'parent':'about-us',
                               'test_count':test_count,
                               'left_ts': left,
                               'middle_ts': middle,
                               'right_ts': right,
                               'paginator': page,
                               'pages': ['about-us', 'testimonials'],
                               'page_name': 'testimonials'})

def testimonial(request, testimonial_id):
    try:
        testimonial = Textimonial.objects.get(id=testimonial_id, display=True)
    except Textimonial.DoesNotExist:
        try:
            return HttpResponsePermanentRedirect("/pa/testimonials/")
        except:
            raise Http404

    return simple_dtt(request, 'about-us/single-testimonial.html', {
                               'parent':'about-us',
                               'testimonial': testimonial,
                               'pages': ['about-us', 'testimonials'],
                               'page_name': 'single-testimonial'})

def view_vidimonials(request):
    testimonials = Vidimonial.objects.order_by('-date_created')

    paginator = Paginator(testimonials, 3)
    page_num = request.GET.get('page', 1)
    page = paginator.page(page_num)

    left = []
    middle = []
    right = []
    loop_counter = 0
    for testimonial in page.object_list:
        if loop_counter == 0:
            left.append({'type': testimonial.__class__.__name__, 'obj': testimonial})
        elif loop_counter == 1:
            middle.append({'type': testimonial.__class__.__name__, 'obj': testimonial})
        elif loop_counter == 2:
            right.append({'type': testimonial.__class__.__name__, 'obj': testimonial})

        if loop_counter == 2:
            loop_counter = 0
        else:
            loop_counter = loop_counter + 1

    return simple_dtt(request, 'about-us/testimonials.html', {
                               'parent':'about-us',
                               'left_ts': left,
                               'middle_ts': middle,
                               'right_ts': right,
                               'paginator': page,
                               'pages': ['about-us', 'testimonials'],
                               'page_name': 'video-testimonials'})

def vidimonial(request, testimonial_id):
    try:
        testimonial = Vidimonial.objects.get(id=testimonial_id)
    except Vidimonial.DoesNotExist:
        raise Http404

    return simple_dtt(request, 'about-us/video-testimonial.html', {
                               'parent':'about-us',
                               'testimonial': testimonial,
                               'pages': ['about-us', 'testimonials'],
                               'page_name': 'single-testimonial'})
