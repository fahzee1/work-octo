from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

from contact.forms import PAContactForm, BasicContactForm, OrderForm

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
    else:
        formset = BasicContactForm()

    return render_to_response('contact-us/index.html', 
                              {'parent':'contact-us',
                               'formset': formset}, 
                              context_instance=RequestContext(request))

def ceo(request):
    if request.method == "POST":
        formset = PAContactForm(request.POST)
        if formset.is_valid():
            formset.save()
    else:
        formset = PAContactForm()

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
            formset.save()
    else:
        formset = OrderForm()

    if 'package' in request.GET:
        formset.fields['package'].initial = request.GET['package']

    return render_to_response('order/order-package.html',
                              {'parent': 'packages',
                               'formset': formset},
                              context_instance=RequestContext(request))
