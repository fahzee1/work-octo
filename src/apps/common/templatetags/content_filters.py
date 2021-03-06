from django import template
from django.template.defaultfilters import stringfilter
import re
register = template.Library()

@register.filter(name="format_number")
@stringfilter
def format_number(variable, pattern=None):
    if pattern is None:
        pattern = r'1-\1-\2-\3'
    return re.sub(r'(\d{3})(\d{3})(\d{4})', r'%s' % pattern, variable)


@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__
