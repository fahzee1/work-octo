from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect

from apps.testimonials.models import Testimonial, Textimonial
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
                               'page_name': 'send-testimonial'})

def view_testimonials(request):
    testimonials = Testimonial.objects.order_by('-date_created')
    left = []
    middle = []
    right = []
    loop_counter = 0
    for testimonial in testimonials:
        if loop_counter == 0:
            left.append(testimonial)
        elif loop_counter == 1:
            middle.append(testimonial)
        elif loop_counter == 2:
            right.append(testimonial)

        if loop_counter == 2:
            loop_counter = 0
        else:
            loop_counter = loop_counter + 1

    return simple_dtt(request, 'about-us/testimonials.html', {
                               'parent':'about-us',
                               'left_ts': left,
                               'middle_ts': middle,
                               'right_ts': right,
                               'page_name': 'testimonial'})