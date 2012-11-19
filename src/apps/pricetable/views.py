from decimal import Decimal

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from apps.common.views import simple_dtt

from shopping_cart import Cart
from models import Package
from forms import EcomForm

def mobile_render(request, template, context):
    if 'current_cart' not in context:
        cart = Cart(request)
        context['current_cart'] = cart
    return simple_dtt(request, template, context)

def mobile_cart_checkout(request):
    context = {}
    context['page_name'] = 'cart-checkout'
    cart = Cart(request)
    context['current_cart'] = cart
    code = cart.get_package_code()
    context['packagecode'] = code
    return simple_dtt(request, 'mobile/cart-checkout.html',
        context)

def index(request):
    context = {}
    context['page_name'] = 'index'
    return mobile_render(request, 'mobile/index.html', context)

def home_security(request):
    context = {}
    context['page_name'] = 'index'
    return mobile_render(request, 'mobile/home-security.html', context)

def interactive(request):
    context = {}
    context['page_name'] = 'interactive'
    return mobile_render(request, 'mobile/interactive.html', context)

def quote(request):
    context = {}
    context['page_name'] = 'quote'
    return mobile_render(request, 'mobile/index.html', context)


def packages(request):
    context = {}
    context['page_name'] = 'packages'
    return mobile_render(request, 'mobile/packages.html', context)

def customer_info(request):
    context = {}
    context['page_name'] = 'customer-info'
    if request.method == 'POST':
        form = EcomForm(request.POST)
        if form.is_valid():
            formset = form.save(commit=False)
            cleaned_data = form.cleaned_data
            name = '%s %s' % (cleaned_data['first_name'],
                              cleaned_data['last_name'])
            address = '%s %s' % (cleaned_data['address'],
                                 cleaned_data['address_2'])
            formset.name = name
            formset.address = address
            formset.save()
            return HttpResponseRedirect(reverse('cart-checkout'))
            
    else:
        form = EcomForm()
    context['form'] = form
    return mobile_render(request, 'mobile/customer-info.html', context)


def monitoring(request):
    context = {}
    context['page_name'] = 'monitoring'
    return mobile_render(request, 'mobile/monitoring.html', context)

def adds(request):
    context = {}
    context['page_name'] = 'add-ons'
    cart = Cart(request)
    if len(cart.equipment) == 2:
        return HttpResponseRedirect(reverse('cart-checkout'))
    context['current_cart'] = cart
    return mobile_render(request, 'mobile/adds.html', context)

def add_to_cart(request):
    context = {}
    price = request.GET.get('price', None)
    monthly = request.GET.get('monthly', None)
    item = request.GET.get('item', None)
    category = request.GET.get('category', None)

    if price == None or monthly == None or item == None or category == None:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    cart = Cart(request)
    cart.add_to_cart(category, item, price, monthly)
    
    return HttpResponseRedirect(reverse('cart'))

def remove_from_cart(request):
    context = {}
    item = request.GET.get('item', None)
    category = request.GET.get('category', None)
    if item == None or category == None:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    cart = Cart(request)
    cart.remove_from_cart(category, item)
    return HttpResponseRedirect(reverse('cart'))

def mobile_cart(request):
    context = {}
    context['page_name'] = 'index'

    return mobile_render(request, 'mobile/cart.html', context)

