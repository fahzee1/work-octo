from django import template
from django.template.defaultfilters import stringfilter
import re
register = template.Library()

@register.filter(name="format_number")
@stringfilter
def format_number(variable, pattern):
        return re.sub(r'(\d{3})(\d{3})(\d{4})', r'%s' % pattern, variable)

