import re
import pdb
from urlparse import parse_qs
from datetime import datetime

from django import template
from sekizai.context import SekizaiContext
from django.conf import settings

from apps.testimonials.models import Testimonial, Textimonial

register = template.Library()
"limit=5&template=local&state={{ state }}&words=100" 

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
            testimonials = Textimonial.objects.filter(permission_to_post=True,
                display=True).order_by('-date_created')
        else:
            testimonials = Textimonial.objects.filter(permission_to_post=True,
                message__icontains=self.search_term,
                display=True).order_by('-date_created')
        
        # filter the testimonials by city
        if 'city' in self.kwargs:
            if self.kwargs['city'][0] == "{{ city }}":
                testimonials = testimonials.filter(city=context['city'])
            else:
                testimonials = testimonials.filter(city=self.kwargs['city'][0])
        # filter the testimonials by state
        if 'state' in self.kwargs:
            if testimonials:
                if self.kwargs['state'][0] == "{{ state }}":
                    testimonials = testimonials.filter(state=context['state'])
                else:
                    testimonials = testimonials.filter(state=self.kwargs['state'][0])
            else:
                testimonials = Textimonial.objects.filter(permission_to_post=True,
                display=True).order_by('-date_created')
                if self.kwargs['state'][0] == "{{ state }}":
                    testimonials = testimonials.filter(state=context['state'])
                else:
                    testimonials = testimonials.filter(state=self.kwargs['state'][0])
        # limit the testimonials by the kwarg
        if 'limit' in self.kwargs:
            testimonials = testimonials[:self.kwargs['limit'][0]]
            
        # bold the search term
        for testimonial in testimonials:
            if self.search_term != '':
                pattern = re.compile(r'(%s)' % self.search_term, re.I)
                testimonial.message = re.sub(pattern,
                    r'<strong>\1</strong>',
                    testimonial.message)
            try:
                date_created = testimonial.date_created.strftime("%m/%d/%Y")
            except AttributeError:
                date_created = datetime.today().strftime("%m/%d/%Y")
                
            testimonial_array.append({'first_name': testimonial.first_name,
              'last_name': testimonial.last_name,
              'city': testimonial.city,
              'state': testimonial.state,
              'date_created': date_created,
              'testimonial': testimonial.message,
              'get_absolute_url': testimonial.get_absolute_url(),
              'date_created': testimonial.date_created})
        t = template.loader.get_template('testimonials/testimonial_3.html')
        c = SekizaiContext({
            'testimonials': testimonial_array,
            'template': self.template,
            'words': self.words
        })
        return t.render(c)
register.tag(testimonial_search)
