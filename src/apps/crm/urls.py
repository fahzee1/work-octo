from django.conf.urls.defaults import *

urlpatterns = patterns('apps.crm.views',

    # account auth urls
    url(r'^login/$', 'crm_login', name="login"),

    # affiliates
    url(r'affiliates/$', 'affiliates', name='affiliates'),
    url(r'affiliates/add/$', 'affiliates_add', name='affiliates_add'),
    url(r'affiliates/(?P<affiliate_id>\d+)/edit/$', 'affiliates_edit',
        name='affiliates_edit'),
    url(r'affiliates/(?P<affiliate_id>\d+)/delete/$', 'affiliates_delete',
        name='affiliates_delete'),
    url(r'affiliates/search/$', 'affiliates_search', name='affiliates_search'),

    # textimonials
    url(r'textimonials/$', 'textimonials', name='textimonials'),
    url(r'textimonials/unread/$', 'textimonials_unread', name='textimonials_unread'),
    url(r'textimonial/display/$', 'textimonials_display',
        name='textimonials_display'),
    url(r'textimonial/dont-display/$', 'textimonials_dont_display',
            name='textimonials_dont_display'),
    url(r'textimonial/(?P<textimonial_id>\d+)/view/$', 'textimonial_view',
        name='textimonial_view'),
    url(r'textimonial/(?P<textimonial_id>\d+)/approve/$', 'textimonial_approve',
        name='textimonial_approve'),
    url(r'textimonial/(?P<textimonial_id>\d+)/dont-display/$', 'textimonial_dont_display',
        name='textimonial_dont_display'),

    url(r'ceo-feedbacks/$', 'ceo_feedbacks', name='ceo_feedbacks'),
    url(r'ceo-feedbacks/unread/$', 'ceo_feedbacks_unread', name='ceo_feedbacks_unread'),
    url(r'ceo-feedback/(?P<feedback_id>\d+)/view/$', 'feedback_view',
        name='feedback_view'),
    url(r'ceo-feedback/(?P<feedback_id>\d+)/convert/$', 'feedback_convert',
        name='feedback_convert'),

    # profiles
    url(r'requests/$', 'affiliate_requests', name='requests'),
    url(r'requests/(?P<profile_id>\d+)/$', 'affiliate_requests_edit',
        name='affiliate_requests_edit'),
    url(r'requests/(?P<profile_id>\d+)/decline/$', 'affiliate_requests_decline',
        name='affiliate_requests_decline'), 
    
    # pages
    url(r'^$', 'index', name='index'),
)