import urllib
import hashlib

from django.http import HttpResponseRedirect
from django.utils import simplejson

from apps.common.views import simple_dtt
from models import PackageCode

def mobile_cart_checkout(request):
    context = {}
    context['page_name'] = 'cart-checkout'
    if 'paCart' not in request.COOKIES:
        return HttpResponseRedirect()
    
    cart = simplejson.loads(urllib.unquote(request.COOKIES['paCart']))
    mhash = hashlib.md5(request.COOKIES['paCart']).hexdigest()
    if 'carthash' in request.session and mhash == request.session['carthash']:
        context['packagecode'] = request.session['packagecode']
        return simple_dtt(request, 'mobile/cart-checkout.html',
        context)

    packagecode = PackageCode()
    packagecode.cart = cart
    packagecode.generate_code()
    packagecode.save()
    context['packagecode'] = packagecode.code
    request.session['packagecode'] = packagecode.code
    request.session['carthash'] = mhash
    return simple_dtt(request, 'mobile/cart-checkout.html',
        context)