from django.contrib.sitemaps import Sitemap

from apps.crimedatamodels.models import CityLocation

class CrimeStatsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return CityLocation.objects.all()

