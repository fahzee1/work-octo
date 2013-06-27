import os
import datetime
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse



class StaticSitemap(Sitemap):
	
	def __init__(self,names,priority):
		self.names=names
		self.pri=priority

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
