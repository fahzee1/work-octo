from django.conf.urls.defaults import *

urlpatterns = patterns('apps.crm.views',

    # account auth urls
    url(r'^login/$', 'crm_login', name="login"),
    url(r'^logout/$', 'crm_logout', name="logout"),

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

    # ceo feedbacks
    url(r'ceo-feedbacks/$', 'ceo_feedbacks', name='ceo_feedbacks'),
    url(r'ceo-feedbacks/unread/$', 'ceo_feedbacks_unread', name='ceo_feedbacks_unread'),
    url(r'ceo-feedbacks/read/$', 'ceo_feedbacks_read', name='ceo_feedbacks_read'),
    url(r'ceo-feedback/(?P<feedback_id>\d+)/view/$', 'feedback_view',
        name='feedback_view'),
    url(r'ceo-feedback/(?P<feedback_id>\d+)/convert/$', 'feedback_convert',
        name='feedback_convert'),

    url(r'ceo-feedbacks/general/$', 'ceo_feedbacks_general', name='ceo_feedbacks_general'),
    url(r'ceo-feedbacks/positive/$', 'ceo_feedbacks_positive', name='ceo_feedbacks_positive'), 
    url(r'ceo-feedbacks/negative/$', 'ceo_feedbacks_negative', name='ceo_feedbacks_negative'), 
    url(r'ceo-feedbacks/other/$', 'ceo_feedbacks_other', name='ceo_feedbacks_other'),
    url(r'ceo-feedbacks/converted/$', 'ceo_feedbacks_posted', name='ceo_feedbacks_postedsite'),

    #temporary cities
    url(r'ceo-feedbacks/newyork/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_newyork'),
    url(r'ceo-feedbacks/boston/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_boston'),
    url(r'ceo-feedbacks/losanageles/$','ceo_feedbacks_cities', name='ceo_feedbacks_losangeles'),
    url(r'ceo-feedbacks/atlanta/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_atlanta'),
    url(r'ceo-feedbacks/chicago/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_chicago'),
    url(r'ceo-feedbacks/dallas/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_dallas'),
    url(r'ceo-feedbacks/detroit/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_detroit'),
    url(r'ceo-feedbacks/houston/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_houston'),
    url(r'ceo-feedbacks/miami/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_miami'),
    url(r'ceo-feedbacks/minneapolis/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_minneapolis'),
    url(r'ceo-feedbacks/philadelphia/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_philadelphia'),
    url(r'ceo-feedbacks/phoenix/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_phoenix'),
    url(r'ceo-feedbacks/sanjose/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_sanjose'),
    url(r'ceo-feedbacks/seattle/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_seattle'),
    url(r'ceo-feedbacks/washington/$', 'ceo_feedbacks_cities', name='ceo_feedbacks_washington'),

    # profiles
    url(r'requests/$', 'affiliate_requests', name='requests'),
    url(r'requests/(?P<profile_id>\d+)/$', 'affiliate_requests_edit',
        name='affiliate_requests_edit'),
    url(r'requests/(?P<profile_id>\d+)/decline/$', 'affiliate_requests_decline',
        name='affiliate_requests_decline'), 

    # search
    url(r'^search$', 'search', name='search'),
    
    # pages
    url(r'^$', 'index', name='index'),
)