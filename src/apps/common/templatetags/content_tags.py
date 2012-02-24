from datetime import datetime

from django import template
from django.conf import settings

from apps.common.models import SpunContent

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

def content_spinner(parser, token):
    tag_name = None
    content_name = None
    content_replacements = None
    try:
        tag_name, content_name, content_replacements = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires at least 3 arguments' %
            token.contents.split()[0])

    return ContentSpinnerNode(content_name[1:-1], content_replacements[1:-1])

class ContentSpinnerNode(template.Node):
    def __init__(self, content_name, content_replacements):
        self.request = template.Variable('request')
        self.name = content_name
        self.replacements = content_replacements.split('|')

    def render(self, context):
        request = self.request.resolve(context)
        path = request.META['PATH_INFO']
        # first try to see if the content has already been spun
        try:
            content = SpunContent.objects.get(url=path, name=self.name)
        except SpunContent.DoesNotExist:
            # get the random choice
            from random import choice
            content = SpunContent()
            content.url = path
            content.name = self.name
            content.content = choice(self.replacements)
            content.save()
        return content.content
register.tag(content_spinner)
