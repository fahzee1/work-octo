import re

from django import template
from django.conf import settings

from apps.testimonials.models import Testimonial

register = template.Library()


def testimonial_search(parser, token):
    try:
        tag_name, search_term = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly one arguments" % 
            token.contents.split()[0])
    return TestimonialSearchNode(search_term[1:-1])

class TestimonialSearchNode(template.Node):
    def __init__(self, search_term):
        self.search_term = search_term
    
    def render(self, context):
        testimonial_array = []
        try:
            testimonials = Testimonial.objects.filter(testimonial__icontains=self.search_term)
            html = ''
            
            for testimonial in testimonials:
                testimonial_html = re.sub(self.search_term,
                    '<strong>%s</strong>' % self.search_term,
                    testimonial.testimonial)

                testimonial_array.append({'first_name': testimonial.first_name,
                  'last_name': testimonial.last_name,
                  'city': testimonial.city,
                  'state': testimonial.state,
                  'date_created': testimonial.date_created.strftime("%m/%d/%Y"),
                  'testimonial': testimonial_html})
                t = template.loader.get_template('testimonials/testimonial_search_tag.html')
                c = template.Context({
                    'testimonials': testimonial_array,
                })
            return t.render(c)
        except:
            return ''
register.tag('testimonial_search', testimonial_search)
