from django.http import HttpResponseRedirect
from django.template import loader, Context
from django.core.mail import send_mail
from django.contrib import messages

from apps.contact.forms import QuestionForm
from apps.common.views import simple_dtt

from models import Question, Tip

def expert_home(request):
    questions = Question.objects.filter(
        expert_question=True, active=True).order_by('-date_created')
    tips = Tip.objects.filter(
        expert_question=True, active=True).order_by('-date_created')
    context = {}
    context['questions'] = questions
    context['tips'] = tips
    context['page_name'] = 'home'
    context['form'] = QuestionForm()
    return simple_dtt(request, 'external/ask-security-expert/index.html', context)

def ask_question(request):

    if request.method == "POST":
        formset = QuestionForm(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request,
                '<p>Hey! Thanks for your question! We\'re putting out best experts to it now and we\'ll answer you shortly!</p>')

            subject = 'New Question Submitted'
            t = loader.get_template('faqs/email.html')
            c = Context(formset.cleaned_data)
            send_mail(subject, t.render(c),
                'Protect America <noreply@protectamerica.com>',
                ['pa_marketing@protectamerica.com'], fail_silently=False)
            return HttpResponseRedirect('/')

    else:
        return HttpResponseRedirect(reverse('contact-us'))