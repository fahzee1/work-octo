from django.conf.urls.defaults import *

urlpatterns = patterns('apps.crm.views',

    # account auth urls
    url(r'^login/$', 'crm_login', name="login"),

    # affiliates
    url(r'affiliates/$', 'affiliates', name='affiliates'),
    url(r'affiliates/(?P<affiliate_id>\d+)/edit/$', 'affiliates_edit',
        name='affiliates_edit'),
    url(r'affiliates/new/$', 'affiliate_requests', name='requests'),
    
    # pages
    url(r'^$', 'index', name='index'),
)