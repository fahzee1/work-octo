from django.conf.urls.defaults import *

urlpatterns = patterns('apps.crm.views',

    # account auth urls
    url(r'^login/$', 'crm_login', name="login"),

    # pages
    url(r'^$', 'index', name='index'),
)