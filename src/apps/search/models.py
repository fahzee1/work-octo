import urllib2

from django.db import models
from django.core.urlresolvers import reverse
from urllib2 import urlopen

class KeywordMatch(models.Model):

    keyword = models.CharField(max_length=128)
    page = models.CharField(max_length=128)

    def get_page_details(self):
        try:
            from lxml.html import parse
            # using old pa sitemap
            # url = reverse(self.page)
            # url = 'http://www.protectamerica.com%s' % url
            url = self.page
            doc = parse(url)
            title = doc.xpath('.//title/text()')[0]
            for meta in doc.xpath('.//meta[@name="description"]'):
                description = meta.get('content', None)
            return {'title': title, 'description': description, 'url': url}
        except:
            return None

    def __unicode__(self):
        return self.keyword


    
