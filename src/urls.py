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
    (r'^$', 'direct_to_template', 
        {'template': 'index.html', 'extra_context': 
            {'page_name': 'index'}}),
    (r'^about-us/?$', 'direct_to_template', 
        {'template': 'about_us.html', 'extra_context': 
            {'page_name': 'about_us'}}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
