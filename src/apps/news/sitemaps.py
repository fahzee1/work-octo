from django.contrib.sitemaps import Sitemap

from apps.news.models import Article

class ArticleSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.order_by('-date_created')

    def lastmod(self, obj):
        return obj.date_created

