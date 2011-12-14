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
        try:
            testimonials = Testimonial.objects.filter(testimonial__icontains=self.search_term)
            html = ''
            
            for testimonial in testimonials:
                testimonial_html = re.sub(self.search_term,
                    '<strong>%s</strong>' % self.search_term,
                    testimonial.testimonial)

                html = html + '<li><div class="customer-name"> \
                <h4>%s %s <span>of %s, %s </span></h4> \
                <strong>%s</strong> \
                <a href="/pa/testimonials" class="button-link" \
                >Read More Testimonials</a></div> \
                <p><img src="%simg/extra/testimonial-arrow.png" \
                class="testimonial-arrow"/> %s \
                </p> \
                </li>' % (testimonial.first_name,
                          testimonial.last_name,
                          testimonial.city,
                          testimonial.state,
                          testimonial.date_created.strftime("%m/%d/%Y"),
                          settings.STATIC_URL,
                          testimonial_html)
            return html
        except:
            return ''
register.tag('testimonial_search', testimonial_search)
