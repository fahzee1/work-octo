from django.conf.urls.defaults import *

from apps.crimedatamodels.sitemaps import CrimeStatsSitemap

sitemaps = {
    'crime_articles': CrimeStatsSitemap
}

urlpatterns = patterns('apps.crimedatamodels.views', 
    url(r'^search/$', 'find_city', name='crime-search'),
    url(r'^(?P<state>[A-Z]{2})/(?P<city>[a-zA-Z\-\_0-9\s\(\),\.\'+]+)/?$', 'crime_stats', name='crime-stats'),
    url(r'^(?P<state>[A-Z]{2})/?$', 'choose_city', name='choose-city'),
    url(r'^$', 'choose_state', name='choose-state'),
)

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

)
