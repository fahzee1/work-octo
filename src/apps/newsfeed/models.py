try:
	from django.utils import timezone
	timezone=timezone
except ImportError:
	from datetime import datetime
	timezone=datetime	

from django.db import models
from django.contrib.localflavor.us.us_states import US_STATES
from django.core.exceptions import ValidationError
# Create your models here.



class DateFeed(models.Model):
	date=models.DateField(help_text='Enter Date')

	def __unicode__(self):
		return "%s" % (self.date)

			


class FeedType(models.Model):
	name=models.CharField(max_length=200,blank=True,null=True,help_text='Type of newsfeed? Two words only for simplicity')

	def __unicode__(self):
		return "%s" % (self.name)

	def save(self,*args,**kwargs):
		try:
			first,last=self.name.split()
			_f=first.capitalize()
			_l=last.capitalize()
			name=_f+' '+_l
			self.name=name
		except ValueError:
			raise ValidationError('Name should be two words only')

		super(FeedType,self).save(*args,**kwargs)



class NewsFeed(models.Model):
	name=models.CharField(max_length=200,blank=True,null=True,help_text='Name of this feed message')
	city=models.CharField(max_length=255,blank=True,null=True,default='')
	state=models.CharField(max_length=2,blank=True,null=True,choices=US_STATES,default='Choose State')
	date_feed=models.ForeignKey(DateFeed,help_text="Enter date for feed to show. If date not here create a new 'date feed'")
	message=models.TextField(blank=False,null=False,help_text='Message to show on feed')
	link=models.URLField(max_length=200,blank=True,null=True,help_text='Link to relevant page')
	icon=models.CharField(max_length=200,blank=True,null=True,help_text='Icon/Image to show with this feed')
	expires=models.DateField(blank=False,null=False,help_text='When does this feed expire?')
	type=models.ForeignKey(FeedType,help_text='What type of feed is this?')
	created=models.DateTimeField(default=timezone.now(),auto_now_add=True)
	active=models.BooleanField(default=True)

	def __unicode__(self):
		return "%s-(%s,%s-%s)" % (self.name,self.type,self.created,self.expires)


	def save(self,*args,**kwargs):
		if not self.date_feed:
			if not self.city:
				if not self.state:
					raise ValidationError('Need a date_feed or city and state')
		if self.city== '' and self.state =='Choose State':
			if not self.date_feed:
				raise ValidationError('Need a date_feed or city and state')
		cap=self.city.capitalize()
		self.city=cap		
		super(NewsFeed,self).save(*args,**kwargs)


	def location(self):
		return "%s,%s" % (self.city,self.state)


	def feed_expired(self):
		if timezone.now() >= self.expires:
			self.active=False
			self.save()


	




