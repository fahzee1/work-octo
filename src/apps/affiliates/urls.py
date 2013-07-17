from django.conf.urls.defaults import *
from django.views.generic.base import RedirectView 


urlpatterns = patterns('apps.affiliates.views',
	url(r'^login$', 'aff_login', name='aff-login'), 
    url(r'^resources/?$', 'get_started_page', name='affiliate_resources'),
    url(r'^(?P<affiliate>[a-zA-Z0-9]+)/?$', 'affiliate_view', name='affiliate'),
    url(r'^(?P<affiliate>[a-zA-Z0-9]+)/(?P<page_name>.*)/?$', 'affiliate_view', name='affiliate_inside'),
    url(r'^request-agent-id/$', 'request_agent_id', name='request_agent_id'),
    ('affiliate/resources/?$',
    	RedirectView.as_view(url='affiliates/resources/get-started',permanent=True)),
    
)
