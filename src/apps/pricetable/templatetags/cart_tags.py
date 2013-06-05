from datetime import datetime

from django import template
from django.conf import settings

from apps.pricetable.models import Package

register = template.Library()

def package_monitoring_price(package, monitoring):
        if monitoring == 'broadband':
            price = package.broadband_monitoring
        elif monitoring == 'cellular':
            price = package.cellular_monitoring
        else:
            price = package.standard_monitoring
        return '$%s' % price

def package_price(parser, token):
    tag_name = None
    package = None
    monitoring = None
    try:
        tag_name, package, monitoring = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires at least 3 arguments' %
            token.contents.split()[0])

    return PackagePriceNode(package.replace('"', ''), monitoring.replace('"', ''))

class PackagePriceNode(template.Node):
    def __init__(self, package, monitoring):
        self.package = package
        self.monitoring = template.Variable(monitoring)

    def render(self, context):
        package = self.package
        try:
            monitoring = self.monitoring.resolve(context)
        except template.VariableDoesNotExist:
            monitoring = 'landline'
        if package == 'basic':
            return package_monitoring_price(Package.objects.get(name='COPPER'),
                                            monitoring)
        elif package == 'standard':
            return package_monitoring_price(Package.objects.get(name='SILVER'),
                                            monitoring)
        elif package == 'premier':
            return package_monitoring_price(Package.objects.get(name='PLATINUM'),
                                            monitoring)
        return ''
register.tag(package_price)


def monitoring_price(parser, token):
    tag_name = None
    package = None
    monitoring = None
    try:
        tag_name, package, monitoring = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires at least 3 arguments' %
            token.contents.split()[0])

    return MonitoringPriceNode(package.replace('"', ''), monitoring.replace('"', ''))

class MonitoringPriceNode(template.Node):
    def __init__(self, package, monitoring):
        self.package = template.Variable(package)
        self.monitoring = monitoring

    def render(self, context):
        try:
            package = self.package.resolve(context)
        except template.VariableDoesNotExist:
            package = 'basic'
        monitoring = self.monitoring
        if package == 'basic':
            return package_monitoring_price(Package.objects.get(name='COPPER'),
                                            monitoring)
        elif package == 'standard':
            return package_monitoring_price(Package.objects.get(name='SILVER'),
                                            monitoring)
        elif package == 'premier':
            return package_monitoring_price(Package.objects.get(name='PLATINUM'),
                                            monitoring)
        return ''
register.tag(monitoring_price)
