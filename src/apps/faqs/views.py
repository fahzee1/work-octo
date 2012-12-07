from models import Question, Tip

from apps.common.views import simple_dtt

def expert_home(request):
    questions = Question.objects.filter(
        expert_question=True, active=True).order_by('-date_created')
    tips = Tip.objects.filter(
        expert_question=True, active=True).order_by('-date_created')
    context = {}
    context['questions'] = questions
    context['tips'] = tips
    context['page_name'] = 'home'
    return simple_dtt(request, 'external/ask-security-expert/index.html', context)