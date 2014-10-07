import pdb
from django import template
from django.utils.safestring import SafeString
from apps.common.models import AbTest, AbTestCode
from django.template import Template, RequestContext
from django.core.cache import cache
from random import choice

register = template.Library()

@register.inclusion_tag('tests/ab.html')
def start_ab(request,test=None):
    code = None
    cookie = request.COOKIES.get('refer_id',None)
    agent_id = request.session.get('refer_id',cookie)
    if agent_id == 'HOMESITE':
        try:
            abtest = request.session.get(test,None)
            abtest_last = cache.get(test)
            test_obj = AbTest.objects.get(name=test)
            if not abtest:
                if test_obj.code_choices:
                    all = test_obj.code_choices.all()
                    if not abtest_last:
                        code = choice(all)
                        aff_id = code.aff_id
                        name = code.name
                        code = code.code
                    else:
                        code = all.exclude(name=abtest_last)
                        if code:
                            code = code[0]
                            aff_id = code.aff_id
                            name = code.name
                            code = code.code

                    if code and name:
                        # set the chosen to test code with the test as the key
                        request.session[test] = name
                        cache.set(test,name)

                        # if agent_id isnt HOMESITE, set it to aff_id value
                        if aff_id != agent_id:
                            request.session['refer_id'] = aff_id
                            request.session['ab_refer_id'] = aff_id

                else:
                    code = '<b>A/B test error. Test name %s doesnt have code choices set, go create AbTestCode in the admin' % test

            else:
                if test_obj.code_choices:
                    try:
                        code = test_obj.code_choices.get(name=abtest)
                        aff_id = code.aff_id
                        code = code.code
                        # if agent_id isnt HOMESITE, set it to aff_id value
                        if aff_id != agent_id:
                            request.session['refer_id'] = aff_id
                            request.session['ab_refer_id'] = aff_id


                    except AbTestCode.DoesNotExist:
                        code = '<b>A/B test error. Test name %s doesnt have code choices with agent_id %s' % (test,agent_id)

                else:
                    code = '<b>A/B test error. Test name %s doesnt have code choices set or agent id isnt set' % test


        except AbTest.DoesNotExist:
            code = '<b>A/B test error. Test name %s doesnt exist, go create it in the admin' % (test if test else "'N/A'")



        # must load tags so django template can render it
        firstline = "{% load content_filters content_tags sekizai_tags testimonial_tags humanize %}\n{% load url from future %}\n"
        code = firstline + code
        t = Template(code)
        code = t.render(RequestContext(request))

        ctx = {'code':code,
           'name':test}
        return ctx
    else:

        return None


