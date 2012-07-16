from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from apps.crm.forms import LoginForm

def crm_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', None)
            password = form.cleaned_data.get('password', None)

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('crm:index'))
    else:
        form = LoginForm()

    return render_to_response('crm/login.html', {
            'form': form,
        }, context_instance=RequestContext(request))

def index(request):
    return render_to_response('crm/index.html', {
        }, context_instance=RequestContext(request))