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
    (r'^admin/', include(admin.site.urls)),

    #contact us
    #url(r'^contact-us/post/?$', 'apps.contact.views.post'),
    #url(r'^contact-us/?$', 'apps.contact.views.main', name='contact-us'),
    #url(r'^contact-us/feedback-to-the-ceo/?$', 'apps.contact.views.ceo',
    #    name='feedback-ceo'),
    #url(r'^contact-us/find-us/?$', 'apps.contact.views.find_us', name='find-us'),
    #url(r'^products/order-package/?$', 'apps.contact.views.order_form',
    #    name='order-package'),
    #url(r'^sitemap/$', 'apps.sitemaps.views.index', name='sitemap'),
)

# a simple direct_to_template wrapper
def dtt(pattern, template, name, parent=None, ctx=None):
    ctx = ctx or {}


    context = dict(page_name=name, parent=parent)
    context.update(ctx)

    return url(pattern, 'apps.common.views.simple_dtt',
		dict(template=template, extra_context=context),
		name=name)

urlpatterns += patterns('',

    # Home Page
   	dtt(r'^$', 'home.html', 'home', ctx={'page_name': 'index'}),

    dtt(r'^products/?$', 'products/_base.html', 'products', ctx={'page_name': 'products'}),
    
    # Copper Page
    dtt(r'^products/copper/?$', 'products/copper.html', 'copper', ctx={'page_name': 'copper'}, parent="products"),
    dtt(r'^products/bronze/?$', 'products/bronze.html', 'bronze', ctx={'page_name': 'bronze'}, parent="products"),
)
"""
urlpatterns += patterns('',

    # Home Page
   	dtt(r'^$', 'index.html', 'home', ctx={'page_name': 'index'}),

    # Product Pages
   	dtt(r'^products/?$', 'products/index.html', 'products'),

    	# Product > Packages

   	   	dtt(r'^products/security-packages/?$', 'products/packages/index.html', 'security-packages', 'products'),

   		dtt(r'^products/security-packages/copper/?$', 'products/packages/copper.html', 'copper', 'security-packages'),
   		dtt(r'^products/security-packages/bronze/?$', 'products/packages/bronze.html', 'bronze', 'security-packages'),
   		dtt(r'^products/security-packages/silver/?$', 'products/packages/silver.html', 'silver', 'security-packages'),
   		dtt(r'^products/security-packages/gold/?$', 'products/packages/gold.html', 'gold', 'security-packages'),
   		dtt(r'^products/security-packages/platinum/?$', 'products/packages/platinum.html', 'platinum', 'security-packages'),

   		# Product > Monitoring

   	   	dtt(r'^products/alarm-monitoring/?$', 'products/monitoring/index.html', 'monitoring', 'products'),

   		dtt(r'^products/alarm-monitoring/landline/?$', 'products/monitoring/landline.html', 'landline', 'monitoring'),

    	# Product > Equipment

   		dtt(r'^products/security-equipment/?$', 'products/equipment/index.html', 'equipment', 'products'),

   		    		# Product > Equipment > Sensors

   					dtt(r'^products/security-equipment/sensors/flood-sensor?$', 'products/equipment/flood-sensor.html', 'flood-sensor', 'sensors'),

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


	# Security 101 Pages

   	dtt(r'^security-101/?$', 'security/index.html', 'security-101'),

   		# Security 101 > Security News

   		dtt(r'^security-101/security-news/?$', 'security/security-news.html', 'security-news', 'security-101'),


    # Help Pages

        # Help Pages > Privacy Policy
            dtt(r'^help/privacy-policy/?$', 'help/privacy-policy.html', 'privacy-policy', 'help'),

        # Help Pages > Return Policy
            dtt(r'^help/return-policy/?$', 'help/return-policy.html', 'return-policy', 'help'),

        # Help Pages > State Licenses
            dtt(r'^help/state-licenses/?$', 'help/state-licenses.html', 'state-licenses', 'help'),


)
"""

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
