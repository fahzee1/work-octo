from django.conf.urls.defaults import *


urlpatterns = patterns('apps.affiliates.views',
	url(r'^login$', 'affiliate_login', name='aff-login'), 
    url(r'^resources/?$', 'resources', name='affiliate_resources'),
    url(r'^(?P<affiliate>[a-zA-Z0-9]+)/?$', 'affiliate_view', name='affiliate'),
    url(r'^(?P<affiliate>[a-zA-Z0-9]+)/(?P<page_name>.*)/?$', 'affiliate_view', name='affiliate_inside'),
    url(r'^request-agent-id/$', 'request_agent_id', name='request_agent_id'),

    
)
