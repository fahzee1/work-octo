import re
from urlparse import parse_qs

from django import template
from django.conf import settings

from apps.testimonials.models import Testimonial

register = template.Library()


def testimonial_search(parser, token, *args, **kwargs):
    tag_name = None
    search_term = None
    kwargs_dict = {}
    try:
        # test to see if just search_term is passed
        tag_name, search_term = token.split_contents()
    except ValueError:
        try:
            tag_name, search_term, kwargs = token.split_contents()
            if kwargs != '':
               kwargs_dict = parse_qs(kwargs[1:-1])
        except ValueError:
            raise template.TemplateSyntaxError(
                "%r tag at least one argument" % 
                token.contents.split()[0])


    return TestimonialSearchNode(search_term[1:-1], kwargs_dict)

class TestimonialSearchNode(template.Node):
    def __init__(self, search_term, kwargs):
        self.search_term = search_term
        self.kwargs = kwargs
        self.template = 'default'
        if 'template' in kwargs:
            self.template = self.kwargs['template'][0]
        self.words = None
        if 'words' in kwargs:
            self.words = self.kwargs['words'][0]
    
    def render(self, context):
        testimonial_array = []

        if self.search_term == '':
            testimonials = Testimonial.objects.filter(can_post=True,
                display=True).order_by('-date_created')
        else:
            testimonials = Testimonial.objects.filter(can_post=True,
                display=True, testimonial__icontains=self.search_term
                ).order_by('-date_created')
        
        # filter the testimonials by state
        if 'state' in self.kwargs:
            testimonials = testimonials.filter(state=self.kwargs['state'][0])
        print testimonials
        # limit the testimonials by the kwarg
        if 'limit' in self.kwargs:
            testimonials = testimonials[:self.kwargs['limit'][0]]

        # bold the search term
        for testimonial in testimonials:
            if self.search_term != '':
                testimonial.testimonial = re.sub(self.search_term,
                    '<strong>%s</strong>' % self.search_term,
                    testimonial.testimonial)

            testimonial_array.append({'first_name': testimonial.first_name,
              'last_name': testimonial.last_name,
              'city': testimonial.city,
              'state': testimonial.state,
              'date_created': testimonial.date_created.strftime("%m/%d/%Y"),
              'testimonial': testimonial.testimonial})
        t = template.loader.get_template('testimonials/testimonial_search_tag.html')
        c = template.Context({
            'testimonials': testimonial_array,
            'template': self.template,
            'words': self.words
        })
        return t.render(c)
register.tag(testimonial_search)
