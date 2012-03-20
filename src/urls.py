from django.conf.urls.defaults import *
from django.conf import settings

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
    (r'^django-admin/', include(admin.site.urls)),

    #contact us
    url(r'^contact/ajaxpost/?$', 'apps.contact.views.ajax_post'),
    url(r'^contact-us/?$', 'apps.contact.views.main', name='contact-us'),
    
    url(r'^contact-us/find-us/?$', 'apps.contact.views.find_us', name='find-us'),
    url(r'^products/order-package/?$', 'apps.contact.views.order_form',
        name='order-package'),
    url(r'^sitemap/$', 'apps.sitemaps.views.index', name='sitemap'),
    
    url(r'^contact-us/feedback-to-the-ceo/?$',
        'apps.testimonials.views.ceofeedback',
        name='feedback-ceo'),

    # affiliate urls
    url(r'^affiliate/resources/?$', 'apps.affiliates.views.resources', name='affiliate_resources'),
    url(r'^affiliate/(?P<affiliate>[a-zA-Z0-9]+)/?$', 'apps.affiliates.views.affiliate_view', name='affiliate'),
    url(r'^affiliate/(?P<affiliate>[a-zA-Z0-9]+)/(?P<page_name>.*)/?$', 'apps.affiliates.views.affiliate_view', name='affiliate_inside'),
    url(r'^sky/?$', 'apps.affiliates.views.delta_sky', name='sky'),

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
        url(r'^(?P<state>[A-Z]{2})/(?P<city>[a-zA-Z\-\_0-9\s+\(\),\']+)/?$', 'apps.local.views.local_page',
        name='local-page'),
        url(r'^(?P<state>[A-Z]{2})/?$', 'apps.local.views.local_city',
        name='choose-city'), 
        url(r'^$', 'apps.local.views.local_state', name='local-state'),
    )
else:
    urlpatterns += patterns('',

        # Home Page
        dtt(r'^$', 'index.html', 'home', ctx={'page_name': 'index'}),
        dtt(r'^thank-you/?$', 'thank-you/index.html', 'thank-you', ctx={'page_name': 'thank-you'}),


        # Home Security Packages
        dtt(r'^home-security-systems/?$', 'packages/index.html', 'security-packages'),

            # Product > Packages B

            dtt(r'^ge-simon-security-systems/wireless-home-alarm/copper-package/?$', 'packages/copper.html', 'copper', 'security-packages'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/bronze-package/?$', 'packages/bronze.html', 'bronze', 'security-packages'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/silver-package/?$', 'packages/silver.html', 'silver', 'security-packages'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/gold-package/?$', 'packages/gold.html', 'gold', 'security-packages'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/platinum-package/?$', 'packages/platinum.html', 'platinum', 'security-packages'),
            

            # Product > Monitoring

            dtt(r'^products/alarm-monitoring/?$', 'products/monitoring/index.html', 'monitoring', 'products'),

            dtt(r'^products/alarm-monitoring/landline/?$', 'products/monitoring/landline.html', 'landline', 'monitoring'),

            # Product > Equipment

            dtt(r'^products/security-equipment/?$', 'products/equipment/index.html', 'equipment', 'products'),

                        # Product > Equipment > Sensors

                        dtt(r'^products/security-equipment/sensors/flood-sensor?$', 'products/equipment/flood-sensor.html', 'flood-sensor', 'sensors'),
                        dtt(r'^products/security-equipment/sensors/door-window-sensor?$', 'products/equipment/door-window-sensor.html', 'door-window-sensor', 'sensors'),


            # Product > Video

            dtt(r'^products/interactive-video/?$', 'products/video/index.html', 'interactive-video', 'products'),

            # Product > GPS Vehicle Tracking

            dtt(r'^products/gps-vehicle-tracking/?$', 'products/gps/index.html', 'gps', 'products'),

            # Product > Cell Takeover

            dtt(r'^products/existing-security-system/?$', 'products/cell-takeover/index.html', 'cell-takeover', 'products'),

        # About Pages

        dtt(r'^about-us/?$', 'about-us/index.html', 'about-us'),

            # About > Profile

            dtt(r'^about-us/company-profile/?$', 'about-us/profile.html', 'profile', 'about-us'),

            # About > Charities

            dtt(r'^about-us/charities/?$', 'about-us/charities.html', 'charities', 'about-us'),

            # About > Testimonials

            dtt(r'^about-us/testimonials/?$', 'about-us/testimonials.html', 'testimonials', 'about-us'),

            # About > Testimonials

            dtt(r'^about-us/textimonials/?$', 'about-us/textimonials.html', 'textimonials', 'testimonials  '),

        # Crime Stats

        dtt(r'^crime-rate/TX/Pflugerville/?$', 'crime-stats/crime-stats.html', 'crime-stats'),
        


        # Help Pages

        dtt(r'^help/?$', 'help/index.html', 'help'),


            # Help Pages > Privacy Policy
                dtt(r'^help/privacy-policy/?$', 'help/privacy-policy.html', 'privacy-policy', 'help'),

            # Help Pages > Return Policy
                dtt(r'^help/return-policy/?$', 'help/return-policy.html', 'return-policy', 'help'),

            # Help Pages > State Licenses
                dtt(r'^help/state-licenses/?$', 'help/state-licenses.html', 'state-licenses', 'help'),

        # Affiliate Resources
        
        #dtt(r'^affiliate/resources/?$', 'affiliates/resources.html', 'aff'),

    url(r'^news/', include('apps.news.urls', namespace='news')),
    url(r'^crime-rate/', include('apps.crimedatamodels.urls', namespace='crime-rate')),
    url(r'^search/$', 'apps.search.views.search', name='search'),
    url(r'^testimonials/', include('apps.testimonials.urls',
        namespace='testimonials')),

)
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
    
