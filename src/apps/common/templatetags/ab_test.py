from django import template
from django.utils.safestring import SafeString
from apps.common.models import AbTest, AbTestCode
from django.template import Template, RequestContext
from random import choice


register = template.Library()

@register.inclusion_tag('tests/ab.html')
def start_ab(request,test=None):
    #import pdb
    #pdb.set_trace()
    code = None
    agent_id = request.session.get('refer_id',None)
    if agent_id == 'HOMESITE':
        try:
            abtest = request.session.get(test,None)
            test = AbTest.objects.get(name=test)
            if not abtest:
                if test.code_choices:
                    all = test.code_choices.all()
                    code = choice(all)
                    aff_id = code.aff_id
                    name = code.name
                    code = code.code

                    # set the chosen to test code with the test as the key
                    request.session[test.name] = name

                    # if agent_id isnt HOMESITE, set it to aff_id value
                    if aff_id != agent_id:
                        request.session['refer_id'] = agent_id
                        request.session['ab_refer_id'] = agent_id

                else:
                    code = '<b>A/B test error. Test name %s doesnt have code choices set, go create AbTestCode in the admin' % test

            else:
                if test.code_choices:
                    try:
                        code = test.code_choices.get(name=abtest)
                        code = code.code

                    except AbTestCode.DoesNotExist:
                        code = '<b>A/B test error. Test name %s doesnt have code choices with agent_id %s' % (test,agent_id)

                else:
                    code = '<b>A/B test error. Test name %s doesnt have code choices set or agent id isnt set' % test


        except AbTest.DoesNotExist:
            code = '<b>A/B test error. Test name %s doesnt exist, go create it in the admin' % (test if test else "'N/A'")



        firstline = "{% load content_filters content_tags sekizai_tags testimonial_tags humanize %}\n{% load url from future %}\n"
        code = firstline + code
        t = Template(code)
        code = t.render(RequestContext(request))

        ctx = {'code':code,
           'name':test}
        return ctx
    else:
        return None


