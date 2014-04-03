import os
import datetime
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse


class StaticSitemap(Sitemap):
    
    def __init__(self, **kwargs):
        self.names = kwargs.get('name', None)
        self.pri= kwargs.get('priority', None)

    def items(self):
        return self.names

    def lastmod(self,obj):
        return datetime.datetime.now()  

    def changefreq(self,obj):
        return 'monthly'

    def location(self,obj):
       return reverse(obj)
            
    def priority(self,obj):
        return self.pri     


class LocalStateSitemap(Sitemap):
    def __init__(self, **kwargs):
        self.states = kwargs.get('states', None)
        self.pri= kwargs.get('priority', None)
    
    def items(self):
        return self.states

    def lastmod(self,obj):
        return datetime.datetime.now()  

    def changefreq(self,obj):
        return 'monthly'

    def location(self,obj):
       return '/home-security/%s' %(obj.upper())
            
    def priority(self,obj):
        return self.pri 

class CrimeRateSitemap(Sitemap):
    def __init__(self, **kwargs):
        self.states = kwargs.get('states', None)
        self.pri= kwargs.get('priority', None)
    
    def items(self):
        return self.states

    def lastmod(self,obj):
        return datetime.datetime.now()  

    def changefreq(self,obj):
        return 'monthly'

    def location(self,obj):
       return '/crime-rate/%s' %(obj.upper())
            
    def priority(self,obj):
        return self.pri     
    

