from datetime import datetime

from django import template
from django.conf import settings

register = template.Library()

def business_time(parser, token):
    # template block that will display contents only if
    # it is business time
    # relevant info: http://bit.ly/2nk9Fe

    nodelist = parser.parse(('endbusinesstime',))
    parser.delete_first_token()
    return BusinessTimeNode(nodelist)
business_time = register.tag('businesstime', business_time)

class BusinessTimeNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist


    def render(self, context):
        
        if not hasattr(settings, 'BUSINESS_HOURS'):
            return ''

        today = datetime.today()
        try:
            start = datetime.strptime('%s-%s-%s %s' % (
                today.day,
                today.month,
                today.year,
                settings.BUSINESS_HOURS[today.weekday()]['start'],
                ), '%d-%m-%Y %H%M')
            end = datetime.strptime('%s-%s-%s %s' % (
                today.day,
                today.month,
                today.year,
                settings.BUSINESS_HOURS[today.weekday()]['end'],
                ), '%d-%m-%Y %H%M')
            now = datetime.now()
            if start <= now <= end:
                # return html
                return self.nodelist.render(context)
            return ''
        except:
            return ''
