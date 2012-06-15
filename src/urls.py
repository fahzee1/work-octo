from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^protectamerica/', include('protectamerica.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls'))

    # Uncomment the next line to enable the admin:
    # Custom Admin Url
    (r'^django-admin/affiliates/affiliate/add/$',
        'apps.affiliates.views.add_affiliate'),
    (r'^django-admin/affiliates/affiliate/(?P<affiliate_id>\d+)/$',
        'apps.affiliates.views.edit_affiliate'),
    (r'^django-admin/', include(admin.site.urls)),

    #contact us
    url(r'^contact/ajaxpost/?$', 'apps.contact.views.ajax_post'),
    
    url(r'^contact-us/find-us/?$', 'apps.contact.views.find_us', name='find-us'),
    url(r'^products/order-package/?$', 'apps.contact.views.order_form',
        name='order-package'),
    url(r'^sitemap/$', 'apps.sitemaps.views.index', name='sitemap'),
    
    url(r'^contact-us/feedback-to-the-ceo/?$',
        'apps.testimonials.views.ceofeedback',
        name='feedback-ceo'),

    # affiliate urls
    #url(r'^affiliate/resources/?$', 'apps.affiliates.views.resources', name='affiliate_resources'),
    #url(r'^affiliate/(?P<affiliate>[a-zA-Z0-9]+)/?$', 'apps.affiliates.views.affiliate_view', name='affiliate'),
    #url(r'^affiliate/(?P<affiliate>[a-zA-Z0-9]+)/(?P<page_name>.*)/?$', 'apps.affiliates.views.affiliate_view', name='affiliate_inside'),
    url(r'^sky/?$', 'apps.affiliates.views.delta_sky', name='sky'),
    url(r'^affiliate/', include('apps.affiliates.urls', namespace='affiliates')),

)

# a simple direct_to_template wrapper
def dtt(pattern, template, name, parent=None, ctx=None):
    ctx = ctx or {}


    context = dict(page_name=name, parent=parent)
    context.update(ctx)

    return url(pattern, 'apps.common.views.simple_dtt',
		dict(template=template, extra_context=context),
		name=name)

# Radioshack URLS
if settings.SITE_ID == 2:
    urlpatterns += patterns('',
        dtt(r'^$', 'affiliates/radioshack/_base.html', 'home', ctx={'page_name': 'index', 'agent_id': 'a02596'}),
        dtt(r'^thank-you/$', 'affiliates/radioshack/thank-you.html', 'thankyou', ctx={'page_name': 'thankyou', 'agent_id': 'a02596'}),
        dtt(r'^cswitch/$', 'affiliates/radioshack/content_switch.html', 'cswitch', ctx={'page_name': 'index', 'agent_id': 'a02596'}),

    )
# Paid landing site
elif settings.SITE_ID == 3:
    urlpatterns += patterns('',
        url(r'^$', 'apps.affiliates.views.semlanding_home'),
        url(r'^google/?$', 'apps.affiliates.views.semlanding_google'),
        url(r'^grbanner/?$', 'apps.affiliates.views.semlanding_google'),
        url(r'^msn/?$', 'apps.affiliates.views.semlanding_bing'),

    )
elif settings.SITE_ID == 4:
    urlpatterns += patterns('',
        # local pages
        url(r'^(?P<state>[A-Z]{2})/(?P<city>[a-zA-Z\-\_0-9\s+\(\),\'\.]+)/$', 'apps.local.views.local_page',
        name='local-page'),
        url(r'^(?P<state>[A-Z]{2})/$', 'apps.local.views.local_city',
        name='choose-city'), 
        url(r'^$', 'apps.local.views.local_state', name='local-state'),
# 301 perm redirect from / to non-/ on article pages
        ('^(?P<state>[A-Z]{2})/(?P<city>[a-zA-Z\-\_0-9\s+\(\),\'\.]+)$',
            redirect_to, {'url': '/%(state)s/%(city)s/', 'permanent': True}),
        
    )
elif settings.SITE_ID == 5:
    urlpatterns += patterns('',
        dtt(r'^$', 'affiliates/all-the-things/base.html', 'home', ctx={'page_name': 'index', 'agent_id': 'AllTheThings'}),
    )
# 5 Linx landing site
elif settings.SITE_ID == 6:
    urlpatterns += patterns('',
        dtt(r'^$', 'affiliates/five-linx/index.html', 'home', ctx={
            'agent_id': 'a01526'}),
        
        url(r'^contest/$', 'apps.common.views.fivelinxcontest'),
        
        dtt(r'^contest/thanks/?$', 'affiliates/five-linx/contest-thanks.html', 'contest-thanks', 'contest', ctx={
            'agent_id': 'a01526'}),        
        url(r'^contest/winner/$', 'apps.common.views.fivelinxwinner'),
        dtt(r'^copper$', 'affiliates/five-linx/copper.html', 'copper', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt(r'^bronze$', 'affiliates/five-linx/bronze.html', 'bronze', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt(r'^silver$', 'affiliates/five-linx/silver.html', 'silver', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt(r'^gold$', 'affiliates/five-linx/gold.html', 'gold', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt(r'^platinum$', 'affiliates/five-linx/platinum.html', 'platinum', 'security-packages', ctx={
            'agent_id': 'a01526'}),

        dtt(r'^video$', 'affiliates/five-linx/video.html', 'video', ctx={
            'agent_id': 'a01526'}),

        dtt(r'^gps$', 'affiliates/five-linx/gps.html', 'gps', ctx={
            'agent_id': 'a01526'}),
        
        dtt(r'^order$', 'affiliates/five-linx/order.html', 'order', ctx={
            'agent_id': 'a01526'}),
            
        dtt(r'^thank-you/5linx/$', 'affiliates/five-linx/thank-you.html', 'thank-you', ctx={
            'agent_id': 'a01526'}),


    )
elif settings.SITE_ID == 7:
    urlpatterns += patterns('',
        url(r'^', include('apps.blogredirects.urls')),
    )
else:
    urlpatterns += patterns('',

        # Home Page
        dtt(r'^$', 'index.html', 'home', ctx={'page_name': 'index'}),
        url(r'^thank-you/?$', 'apps.common.views.thank_you',
            name='thank_you'),
        url(r'^thank-you/(?P<custom_url>.*)/?$',
        'apps.common.views.thank_you', name='custom_thank_you'),

        # pay it forward page
        url(r'^payitforward/$', 'apps.common.views.payitforward',
            name='payitforward'),

        # Home Security Packages
        dtt(r'^pa/packages/alarms/?$', 'packages/index.html', 'products'),

            # Product > Packages B

            dtt(r'^ge-simon-security-systems/wireless-home-alarm/copper-package/?$', 'packages/copper.html', 'copper', 'products'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/bronze-package/?$', 'packages/bronze.html', 'bronze', 'products'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/silver-package/?$', 'packages/silver.html', 'silver', 'products'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/gold-package/?$', 'packages/gold.html', 'gold', 'products'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/platinum-package/?$', 'packages/platinum.html', 'platinum', 'products'),
            

            # Product > Monitoring

            dtt(r'^pa/monitoring/security-system/?$', 'products/monitoring/index.html', 'monitoring', 'products'),

            dtt(r'^products/alarm-monitoring/landline/?$', 'products/monitoring/landline.html', 'landline', 'monitoring'),

            # Product > Equipment

            dtt(r'^pa/equipment/wireless-home-security-system/?$', 'products/equipment/index.html', 'equipment', 'products'),

                        # Product > Equipment > Sensors

                        dtt(r'^products/security-equipment/sensors/flood-sensor?$', 'products/equipment/flood-sensor.html', 'flood-sensor', 'sensors'),
                        dtt(r'^products/security-equipment/sensors/door-window-sensor?$', 'products/equipment/door-window-sensor.html', 'door-window-sensor', 'sensors'),
                        
                        # Product > Equipment > Touch Screen
                        
                        dtt(r'^products/security-equipment/accessories/touchscreen?$', 'products/equipment/touchscreen.html', 'touchscreen', 'accessories'),


            # Product > Video

            dtt(r'^pa/wireless-security-camera/ip-security-cameras/?$', 'products/video/index.html', 'video', 'products'),

            # Product > GPS Vehicle Tracking

            dtt(r'^pa/vehicle-gps-tracking/gps-services/?$', 'products/gps/index.html', 'gps', 'products'),

            # Product > Cell Takeover

            dtt(r'^pa/existing-home-security-system/cellular-monitoring/?$', 'products/cell-takeover/index.html', 'cell-takeover', 'products'),

        # About Pages

        dtt(r'^pa/about/home-security-companies/?$', 'about-us/index.html', 'about-us'),

            # About > Profile

            dtt(r'^pa/profile/home-alarm-systems/?$', 'about-us/profile.html', 'profile', 'about-us'),

            # About > Family of Companies

            dtt(r'^pa/family-of-companies/america-protect/?$', 'about-us/family-of-companies.html', 'family', 'about-us'),

            # About > Charities

            dtt(r'^pa/charities/america-protect/?$', 'about-us/charities.html', 'charities', 'about-us'),
            
            # About > How it Works

            dtt(r'^pa/how_it_works/ge-security-systems/?$', 'about-us/how-it-works.html', 'how-it-works', 'about-us'),

            # About > Learn About Security

            dtt(r'^pa/learn/alarm-companies/?$', 'about-us/learn-about-security.html', 'learn-about-security', 'about-us'),

            # About > Testimonials

            dtt(r'^pa/testimonials/?$', 'about-us/testimonials.html', 'testimonials', 'about-us'),

            # About > Testimonials

            dtt(r'^about-us/textimonials/?$', 'about-us/textimonials.html', 'textimonials', 'testimonials  '),

        # Crime Stats

        dtt(r'^crime-rate/TX/Pflugerville/?$', 'crime-stats/crime-stats.html', 'crime-stats'),
        
        # Complete Home Security 
        
        dtt(r'^complete-home-security/?$', 'complete-home-security/index.html', 'complete-home-security'),
        
        # Contact Pages

        #dtt(r'^contact-us/?$', 'contact-us/index.html', 'contact-us'),
        url(r'^pa/contact/?$', 'apps.contact.views.main', name='contact-us'),
        
        # Contact Pages > Find Us
        dtt(r'^contact/find-us?$', 'contact-us/find-us.html', 'find-us', 'contact-us'),
        
        # Contact Pages > Department Listing
        dtt(r'^contact/department-listing?$', 'contact-us/department-listing.html', 'department-listing', 'contact-us'),


        # Help Pages

        dtt(r'^help/?$', 'help/index.html', 'help'),


            # Help Pages > Privacy Policy
                dtt(r'^help/privacy-policy/?$', 'help/privacy-policy.html', 'privacy-policy', 'help'),

            # Help Pages > Return Policy
                dtt(r'^help/return-policy/?$', 'help/return-policy.html', 'return-policy', 'help'),

            # Help Pages > State Licenses
                dtt(r'^help/state-licenses/?$', 'help/state-licenses.html', 'state-licenses', 'help'),

        # Support Pages
        
        dtt(r'^support/?$', 'support/index.html', 'support'),
        
        # Affiliate Resources
        
        #dtt(r'^affiliate/resources/?$', 'affiliates/resources.html', 'aff'),

    url(r'^news/', include('apps.news.urls', namespace='news')),
    url(r'^crime-rate/', include('apps.crimedatamodels.urls', namespace='crime-rate')),
    url(r'^search/$', 'apps.search.views.search', name='search'),
    url(r'^testimonials/', include('apps.testimonials.urls',
        namespace='testimonials')),
    ('^(?P<agent_id>[A-Za-z0-9\_-]+)/?$',
            'apps.common.views.redirect_wrapper'),
)
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
    
