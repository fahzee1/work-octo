from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url(r'^$', 'apps.sitemaps.sitemap_dyn.index', name='sitemap'),
)
urlpatterns += patterns('django.views.generic.simple',
    url(r'^index.xml$', 'direct_to_template', {
            'template': 'sitemaps/index.xml',
            'mimetype': 'application/xml',
        }, name='index'),
    
    url(r'^main.xml$', 'direct_to_template', {
            'template': 'sitemaps/main.xml',
            'mimetype': 'application/xml',
        }, name='main'),

    url(r'^mobile.xml$', 'direct_to_template', {
            'template': 'sitemaps/mobile.xml',
            'mimetype': 'application/xml',
        }, name='mobile'),

    url(r'^images.xml$', 'direct_to_template', {
            'template': 'sitemaps/images.xml',
            'mimetype': 'application/xml',
        }, name='images'),

    url(r'^videos.xml$', 'direct_to_template', {
            'template': 'sitemaps/videos.xml',
            'mimetype': 'application/xml',
        }, name='videos'),
)
