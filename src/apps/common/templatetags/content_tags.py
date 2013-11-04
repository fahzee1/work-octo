import os
import pdb
import json
from glob import glob
from django.conf import settings
from random import choice
from datetime import datetime
from django import template
from django.conf import settings
from apps.common.models import SpunContent
from apps.local.views import get_statecode
from django.http import Http404
from django.contrib.localflavor.us.us_states import US_STATES

register = template.Library()


def paragraph_spinner(parser,token):
    """
    use will be like this...
    {% paragraph spinner %}
        <p></p>
        <p></p>
        <p></p>
    this paragraph should chose a random paragraph then that 
    random paragraph has spinners within itself alos to spin 
    content

    """
    tag_name = None
    paragraph = None
    try:
        tag_name, paragraph = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError( '%r tag requires at least 1 arguments' % token.contents.split()[0]))
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
        #pdb.set_trace()
        request = self.request.resolve(context)
        path = request.META['PATH_INFO'].rstrip('/').lstrip('/')
        city,state = path.split('/')
        if '.' in city:
            f,l = city.split('.')
            city = f+ '.'+' '+l
        if '-' in city:
            if city.count('st',0,2) == 1:
                f,l = city.split('-')
                city = f+'.'+' '+l
            else:
                city = city.replace('-',' ')
        statecode = get_statecode(state)
        json_file = statecode+'/'+city.title()+'.json'
        default = '/virtual/customer/www2.protectamerica.com/localpages/'
        LOCAL_PAGE_PATH = getattr(settings,'LOCAL_PAGE_PATH',default)
        os.chdir(LOCAL_PAGE_PATH)
        if os.path.exists(json_file):  
            try:
                the_file = open(json_file,'r+')
                new_file = json.load(the_file)
                try:
                    content = new_file[self.name]
                except KeyError:
                    if self.name not in new_file.keys():
                        obj = {self.name:choice(self.replacements)}
                        new_file.update(obj)
                        with open(json_file, 'w+') as f:
                            f.write(json.dumps(new_file))
                        content = new_file[self.name]

            except IOError:
                raise Http404
        else:
            if not os.path.exists(statecode):
                os.makedirs(statecode)
                os.chdir(statecode)
                obj = {self.name:choice(self.replacements)}
                with open(city.title()+'.json',"w+") as f:
                    f.write(json.dumps(obj))
                content = obj[self.name]
            
            elif os.path.exists(statecode):
                os.chdir(statecode)
                j_file = city.title() +'.json'
                try:
                    _files = glob('*json')
                    _list=[]
                    for f in _files:
                        _list.append(f)
                    if j_file not in _list:
                        obj = {self.name:choice(self.replacements)}
                        with open(j_file,"w+") as f:
                            f.write(json.dumps(obj))
                        content = obj[self.name]
                    else:
                        _file = _files[0]
                        try:
                            the_file = open(_file,'r+')
                            new_file = json.load(the_file)
                            try:
                                content = new_file[self.name]
                            except KeyError:
                                raise Http404
                        except IOError:
                            raise Http404

                except:
                    raise Http404
            else:
                os.chdir(statecode+'/'+city.title())
                try:
                    #get first file that ends in json
                    _file = glob('*.json')[0]
                except:
                    raise Http404
                try:    
                    the_file = open(_file,'r+')
                    new_file = json.load(the_file)
                    try:
                        content = new_file[self.name]
                    except KeyError:
                        raise Http404

                except IOError:
                    raise Http404


        if '{{ city }}' in content:
            content = content.replace('{{ city }}',city.title())
        if '{{ state }}' in content:
            content = content.replace('{{ state }}',state.title())
        return content

register.tag(content_spinner)

