import datetime

from django.contrib.sitemaps import Sitemap

from apps.crimedatamodels.models import CityLocation, ZipCode, State

class KeywordStateSitemap(Sitemap):

    def items(self):
        return State.objects.all()

    def lastmod(self, obj):
        return datetime.date(2012, 10, 12)

    def location(self, obj):
        try:
            return '/%s/%s/sitemap.xml' % (
                self.keyword, obj.name)
        except:
            print obj.name

    def __init__(self, keyword, *args, **kwargs):
        self.keyword = keyword
        super(KeywordStateSitemap, self).__init__(*args, **kwargs)

class KeywordCitySitemap(Sitemap):

    def items(self):
        state = State.objects.filter(name=self.state).values('abbreviation')
        if len(state):
            state = state[0]
        return CityLocation.objects.filter(state=state['abbreviation'])

    def lastmod(self, obj):
        return datetime.date(2012, 10, 12)

    def location(self, obj):
        try:
            if obj.state and obj.city_name:
                state = State.objects.get(abbreviation=obj.state)
                return '/%s/%s/%s/%s/' % (
                    self.keyword, obj.city_name.lower().replace(' ', '-'), state.name.lower(), '00000')
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