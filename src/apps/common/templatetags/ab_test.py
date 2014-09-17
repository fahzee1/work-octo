from django import template
from django.utils.safestring import SafeString
from apps.common.models import AbTest, AbTestCode
from random import choice


register = template.Library()

@register.inclusion_tag('tests/ab.html')
def start_ab(request,test=None):
    code = None
    try:
        abtest = request.session.get('abtest',None)
        test = AbTest.objects.get(name=test)
        if not abtest:
            if test.code_choices:
                all = test.code_choices.all()
                code = choice(all)
                agent_id = code.aff_id
                name = code.name
                code = code.code

                request.session['abtest'] = True
                request.session['abtest_name'] = [name]
                request.session['refer_id'] = agent_id

            else:
                code = '<b>A/B test error. Test name %s doesnt have code choices set, go create AbTestCode in the admin' % test

        else:
            agent_id = request.session.get('refer_id',None)
            if test.code_choices and agent_id:
                try:
                    code = test.code_choices.get(aff_id=agent_id)
                    code = code.code

                except AbTestCode.DoesNotExist:
                    code = '<b>A/B test error. Test name %s doesnt have code choices with agent_id %s' % (test,agent_id)

            else:
                code = '<b>A/B test error. Test name %s doesnt have code choices set or agent id isnt set' % test


    except AbTest.DoesNotExist:
        code = '<b>A/B test error. Test name %s doesnt exist, go create it in the admin' % (test if test else "'N/A'")


    ctx = {'code':SafeString(code),
           'name':test}
    return ctx


