import datetime

from django.contrib.sitemaps import Sitemap

from apps.crimedatamodels.models import CityLocation, State

class CrimeStatsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return CityLocation.objects.all()


class FreeCrimeStatsStateSitemap(Sitemap):

    def items(self):
        return State.objects.all()

    def lastmod(self, obj):
        return datetime.date(2012, 10, 12)

    def location(self, obj):
        try:
            return '/free-crime-stats/%s/sitemap.xml' % (obj.slug)
        except:
            print obj.slug

    def __init__(self, *args, **kwargs):
        super(FreeCrimeStatsStateSitemap, self).__init__(*args, **kwargs)

class FreeCrimeStatsCitySitemap(Sitemap):

    def items(self):
        state = State.objects.filter(slug=self.state).values('abbreviation')
        if len(state):
            state = state[0]
        return CityLocation.objects.filter(state=state['abbreviation'])

    def lastmod(self, obj):
        return datetime.date(2012, 10, 12)

    def location(self, obj):
        try:
            return '/free-crime-stats/%s/%s/sitemap.xml' % (obj.state, obj.city_name_slug)
        except:
            print obj.slug

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super(FreeCrimeStatsCitySitemap, self).__init__(*args, **kwargs)

class FreeCrimeStatsCrimeSitemap(Sitemap):

    def items(self):
        return ('',
                'burglary',
                'robbery',
                'motor-vehicle-theft',
                'violent-crime',
                'larceny')

    def lastmod(self, obj):
        return datetime.date(2012, 10, 12)

    def location(self, obj):
        try:
            if obj == '':
                return '/%s/%s/' % (self.state, self.city)
            return '/%s/%s/%s/' % (self.state, self.city, obj)
        except:
            print obj

    def __init__(self, state, city, *args, **kwargs):
        self.state = state
        self.city = city
        super(FreeCrimeStatsCrimeSitemap, self).__init__(*args, **kwargs)