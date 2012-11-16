import urllib
import hashlib
from decimal import Decimal

from django.utils import simplejson

from models import PackageCode, Package

class Cart(object):
    package = {}
    monitoring = {}
    equipment = {}
    request = None
    
    def __init__(self, request):
        self.request = request
        cart = request.session.get('paCart', None)

        if cart == '' or cart is None:
            cart = {
                'package': self.package,
                'monitoring': self.monitoring,
                'equipment': self.equipment
            }
        else:
            cart = simplejson.loads(cart)
        self.cart = cart
        self.package = cart['package']
        self.monitoring = cart['monitoring']
        self.equipment = cart['equipment']

    def get_json(self):
        return simplejson.dumps({
                'package': self.package,
                'monitoring': self.monitoring,
                'equipment': self.equipment
            })

    def reset(self):
        self.package = {}
        self.monitoring = {}
        self.equipment = {}
        return True

    def save(self):
        self.request.session['paCart'] = self.get_json()
        return True

    def add_to_cart(self, category, item, price, monthly):
        if category == 'equipment':
            self.add_equipment(item, price, monthly)
        elif category == 'monitoring':
            self.add_monitoring(item, price, monthly)
        elif category == 'package':
            self.add_package(item, price, monthly)
        self.save()

    def add_monitoring(self, item, price, monthly):
        self.monitoring = {'item': item, 'price': price, 'monthly': monthly}

    def add_package(self, item, price, monthly):
        self.package = {'item': item, 'price': price, 'monthly': monthly}

    def add_equipment(self, item, price, monthly):
        if item not in self.equipment:
            self.equipment[item] = {'price': price, 'count': 0, 'monthly': monthly}
        self.equipment[item]['count'] = (self.equipment[item]['count'] + 1)

    def remove_from_cart(self, category, item):
        if category == 'equipment':
            self.remove_equipment(item)
        elif category == 'monitoring':
            self.remove_monitoring()
        elif category == 'package':
            self.remove_package()
        self.save()

    def remove_monitoring(self):
        self.monitoring = {}

    def remove_package(self):
        self.package = {}

    def remove_equipment(self, item):
        if item not in self.equipment:
            return False
        self.equipment[item]['count'] = (self.equipment[item]['count'] - 1)
        if self.equipment[item]['count'] == 0:
            del self.equipment[item]

    def get_equipment_price(self):
        total = Decimal('0.00')
        for name, info in self.equipment.iteritems():
            equipment_total = Decimal(info['count'] * info['price'])
            total += equipment_total
        return total

    def get_equipment_monthly(self):
        total = Decimal('0.00')
        for name, info in self.equipment.iteritems():
            equipment_monthly = Decimal(info['count'] * info['monthly'])
            total += equipment_monthly
        return total

    def get_cart_price(self):
        total = Decimal('0.00')
        total += self.get_equipment_price()
        if self.package:
            total += Decimal(self.package['price'])
        if self.monitoring:
            total += Decimal(self.monitoring['price'])
        return total

    def get_package_monthly(self):
        total = Decimal('0.00')
        package = None
        if len(self.package) > 0:
            if self.package['item'] == 'basic':
                package = Package.objects.get(name='COPPER')
            elif self.package['item'] == 'standard':
                package = Package.objects.get(name='SILVER')
            elif self.package['item'] == 'premier':
                package = Package.objects.get(name='PLATINUM')

        if len(self.monitoring) > 0:
            if package is None:
                package = Package.objects.get(name='COPPER')
            if self.monitoring['item'] == 'landline':
                total += Decimal(package.standard_monitoring)
            elif self.monitoring['item'] == 'broadband':
                total += Decimal(package.broadband_monitoring)
            elif self.monitoring['item'] == 'cellular':
                total += Decimal(package.cellular_monitoring)
        elif package is not None:
            total += Decimal(package.standard_monitoring)

        return total

    def get_cart_monthly(self):
        total = Decimal('0.00')
        total += self.get_equipment_monthly()
        total += self.get_package_monthly()
        return total

    def get_package_code(self):
        mhash = hashlib.md5(self.get_json()).hexdigest()
        if 'carthash' in self.request.session and mhash == self.request.session['carthash']:
            return self.request.session['packagecode']

        packagecode = PackageCode()
        packagecode.cart = self.get_json()
        packagecode.generate_code()
        packagecode.save()
        
        self.request.session['packagecode'] = packagecode.code
        self.request.session['carthash'] = mhash
        return packagecode.code