from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from apps.crimedatamodels.sitemaps import CrimeStatsSitemap

sitemaps = {
    'crime_articles': CrimeStatsSitemap
}

urlpatterns = patterns('apps.crimedatamodels.views', 
    url(r'^search/$', 'find_city', name='crime-search'),
    url(r'^(?P<state>[A-Z]{2})/(?P<city>[a-zA-Z\-\_0-9\s\(\),\.\'+]+)$', 'crime_stats', name='crime-stats'),
    url(r'^(?P<state>[A-Z]{2})$', 'choose_city', name='choose-city'),
    url(r'^$', 'choose_state', name='choose-state'),
    
    ('^(?P<state>[A-Z]{2})/(?P<city>[a-zA-Z\-\_0-9\s+\(\),\'\.]+)/$',
            redirect_to, {'url': 'http://www.protectamerica.com/crime-rate/%(state)s/%(city)s', 'permanent': True}),
    
)

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

)
