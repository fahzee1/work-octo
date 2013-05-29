import datetime

from django.contrib.sitemaps import Sitemap

from apps.crimedatamodels.models import ZipCode, State

class KeywordStateSitemap(Sitemap):

    def items(self):
        return State.objects.all()

    def lastmod(self, obj):
        return datetime.date(2012, 10, 12)

    def location(self, obj):
        try:
            return '/%s/%s/' % (
                self.keyword, self.state.name)
        except:
            print obj.state

    def __init__(self, keyword, *args, **kwargs):
        self.keyword = keyword
        super(KeywordStateSitemap, self).__init__(*args, **kwargs)

class KeywordCitySitemap(Sitemap):

    def items(self):
        state = State.objects.filter(name=self.state).values('abbreviation')
        if len(state):
            state = state[0]
        return ZipCode.objects.filter(state=state.abbreviation).values('city')

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

    def __init__(self, keyword, state, *args, **kwargs):
        self.keyword = keyword
        self.state = state
        super(KeywordCitySitemap, self).__init__(*args, **kwargs)


class KeywordSitemapIndex(Sitemap):
    def items(self):
        return self.keywords

    def lastmod(self, obj):
        return datetime.date(2012, 10, 12)

    def location(self, obj):
        return '/%s/sitemap.xml' % obj

    def __init__(self, keywords, *args, **kwargs):
        self.keywords = keywords
        super(KeywordSitemapIndex, self).__init__(*args, **kwargs)