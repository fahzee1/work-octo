from decimal import Decimal

from django.http import HttpResponseRedirect

from apps.common.views import simple_dtt

from shopping_cart import Cart
from models import Package

def mobile_render(request, template, context):
    if 'current_cart' not in context:
        cart = Cart(request)
        context['current_cart'] = cart
    return simple_dtt(request, template, context)

def mobile_cart_checkout(request):
    context = {}
    context['page_name'] = 'cart-checkout'
    cart = Cart(request)
    code = cart.get_package_code()    
    context['packagecode'] = code
    context['current_cart'] = cart
    
    return simple_dtt(request, 'mobile/cart-checkout.html',
        context)

def index(request):
    context = {}
    context['page_name'] = 'index'
    return mobile_render(request, 'mobile/index.html', context)

def packages(request):
    context = {}
    context['page_name'] = 'packages'
    return mobile_render(request, 'mobile/packages.html', context)


def customer_info(request):
    context = {}
    context['page_name'] = 'customer-info'
    return mobile_render(request, 'mobile/customer-info.html', context)


def monitoring(request):
    context = {}
    context['page_name'] = 'monitoring'
    return mobile_render(request, 'mobile/monitoring.html', context)

def adds(request):
    context = {}
    context['page_name'] = 'add-ons'
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
    
    return HttpResponseRedirect('/cart/')

def remove_from_cart(request):
    context = {}
    item = request.GET.get('item', None)
    category = request.GET.get('category', None)
    if item == None or category == None:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    cart = Cart(request)
    cart.remove_from_cart(category, item)
    return HttpResponseRedirect('/cart/')

def mobile_cart(request):
    context = {}
    context['page_name'] = 'index'

    return mobile_render(request, 'mobile/cart.html', context)

