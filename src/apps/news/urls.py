from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from apps.news.sitemaps import ArticleSitemap
from apps.news.feeds import RssNewsFeed

news_sitemap = {
    'news_articles': ArticleSitemap,
}
urlpatterns = patterns('apps.news.views',

    url(r'^$', 'news_home', name='news-home'),

    url(r'^archive/$', 'articles', name='news-articles'),
    url(r'^archive/(?P<year>[0-9]{4})/$',
        'articles_by_year', name='news-articles-by-year'),

    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        'articles_by_month', name='news-articles-by-month'),
    
    url(r'^category/(?P<category_name>[a-zA-Z\-\_0-9\s+]+)_(?P<category_id>[0-9]+)/$', 'category', name='news-category'),
    url(r'^brafton-import/$', 'import_articles',
        name='news-import'),
    url(r'^load-more/(?P<last_id>\d+)/',
        'load_more_articles', name="load-more-articles"),
    url(r'^article/(?P<article_title>[a-zA-Z\-\_0-9\s+]+)_(?P<article_id>[0-9]+)$', 'article', name="news-article"),

    # redirect old urls
    url(r'^article/(?P<article_id>\d+)-(.*)/?$', 'redirect_old', name='news-article-redirect'),
    url(r'^category/(?P<category_id>\d+)-(.*)/?$', 'redirect_old_category', name='news-category-redirect'),
    
    # redirect /news/article/ to /news/archive/
    url('^article/$', redirect_to, {'url': '/news/archive/', 'permanent': True}),
    

)

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': news_sitemap}),
    url(r'^rss/$', RssNewsFeed()),

)
