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
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', 
    	dict(template='index.html', extra_context={'page_name': 'index'}), 
    	name='home'),
    # Product Pages
    url(r'^products/?$', 'direct_to_template', 
    	dict(template='products/index.html', extra_context={'page_name': 'products'}), 
    	name='products'),
    	# Products > Package Pages
    	url(r'^products/packages/copper/?$', 'direct_to_template', 
	    	dict(template='products/copper.html', extra_context={'page_name': 'copper'}), 
	    	name='copper'),
	    url(r'^products/packages/bronze/?$', 'direct_to_template', 
	    	dict(template='products/bronze.html', extra_context={'page_name': 'bronze'}), 
	    	name='bronze'),
    url(r'^products/interactive-video/?$', 'direct_to_template', 
    	dict(template='products/video.html', extra_context={'page_name': 'interactive-video'}), 
    	name='interactive-video'),
    # Equipment Pages
    url(r'^products/security-equipment/?$', 'direct_to_template', 
    	dict(template='products/equipment/index.html', extra_context={'page_name': 'equipment'}), 
    	name='equipment'),
    
    # About Pages
    url(r'^about-us/?$', 'direct_to_template', 
    	dict(template='about-us/index.html', extra_context={'page_name': 'about-us'}), 
    	name='about-us'),
   	url(r'^about-us/profile/?$', 'direct_to_template', 
    	dict(template='about-us/profile.html', extra_context={'page_name': 'profile'}), 
    	name='profile'),
    url(r'^about-us/charities/?$', 'direct_to_template', 
    	dict(template='about-us/charities.html', extra_context={'page_name': 'charities'}), 
    	name='charities'),
    # Contact Pages
    url(r'^contact-us/?$', 'direct_to_template', 
    	dict(template='contact-us/index.html', extra_context={'page_name': 'contact-us'}), 
    	name='contact-us'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

