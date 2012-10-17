import datetime

from django.contrib.sitemaps import Sitemap

from apps.crimedatamodels.models import ZipCode, State

class KeywordSitemap(Sitemap):

    def items(self):
        return ZipCode.objects.all()

    def lastmod(self, obj):
        return datetime.date(2012, 10, 12)

    def location(self, obj):
        try:
            if obj.state and obj.city:
                state = State.objects.get(abbreviation=obj.state)
                return '/%s/%s/%s/%s/' % (
                    self.keyword, obj.city.lower().replace(' ', '-'), state.name.lower(), obj.zip)
        except:
            print obj.state

    def __init__(self, keyword, *args, **kwargs):
        self.keyword = keyword
        super(KeywordSitemap, self).__init__(*args, **kwargs)