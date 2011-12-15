from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

from apps.testimonials.models import Testimonial
from apps.testimonials.forms import TestimonialForm, CEOForm

def ceofeedback(request):
    if request.method == 'POST':
        formset = CEOForm(request.POST)
        if formset.is_valid():
            formset.save()
    else:
        formset = CEOForm()

    return render_to_response('contact-us/feedback-ceo.html',
                              {'parent':'contact-us',
                               'formset': formset},
                              context_instance=RequestContext(request))

def post_testimonial(request):
    # this view is to post a testimonial to the website
    # this will be used until the new testimonial pages are ready
    # The purpose of this is to submit the new testimonials to both the
    # old system and the new system so that when the change is made
    # we do not miss any testimonials
    if request.method == 'POST':
        # the post must have 'first_name', 'last_name', 
        # 'city', 'state', 'testimonial' in the submission
        testimonial = TestimonialForm(request.POST)
        if testimonial.is_valid():
            testimonial.save()
    else:
        return Http404
