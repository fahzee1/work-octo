from datetime import datetime

from django import template
from django.conf import settings

from models import Package

register = template.Library()

def content_spinner(parser, token):
    tag_name = None
    package = None
    monitoring = None
    try:
        tag_name, package, monitoring = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires at least 3 arguments' %
            token.contents.split()[0])

    return ContentSpinnerNode(package.replace('"', ''),
                              monitoring.replace('"', ''))

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
