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



			
class AddType(models.Model):
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
			_name=self.name.split()
			if len(_name) ==1:
				_name=self.name.capitalize()
				self.name=_name
			else:
				raise ValidationError('Name should be two words only')

		super(AddType,self).save(*args,**kwargs)



class TheFeed(models.Model):
	name=models.CharField(max_length=200,blank=True,null=True,help_text='Name of this feed message')
	city=models.CharField(max_length=255,blank=True,null=True)
	state=models.CharField(max_length=2,blank=True,null=True,choices=US_STATES)
	visible_to_all=models.BooleanField(default=False,help_text='This feed message will be seen by everyone not just a specific location. No need to enter city/state.')
	message=models.TextField(blank=False,null=False,help_text='Message to show on feed')
	link_name=models.CharField(max_length=255,blank=True,null=True,default='Click Here')
	link=models.URLField(max_length=200,blank=True,null=True,help_text='Link to relevant page')
	icon=models.CharField(max_length=200,blank=True,null=True,help_text='Icon/Image to show with this feed')
	expires=models.DateField(blank=False,null=False,help_text='When does this feed expire?')
	type=models.ForeignKey(AddType,help_text='What type of feed is this?')
	created=models.DateTimeField(default=timezone.now(),auto_now_add=True)
	active=models.BooleanField(default=True)

	def __unicode__(self):
		return "%s-(type:%s,created:%s)" % (self.name,self.type,self.created)


	def save(self,*args,**kwargs):
		if not self.city or not self.state:
			if not self.visible_to_all:
				raise ValidationError('city and state or visible to all required')

		try:
			f,l=self.city.split()
			a=f.capitalize()
			b=l.capitalize()
			comp=a+' '+b
			self.city=comp
		except:
			a=self.city.capitalize()
			self.city=a	
		super(TheFeed,self).save(*args,**kwargs)


	def location(self):
		return "%s,%s" % (self.city,self.state)


	def feed_expired(self):
		if timezone.today().date() >= self.expires:
			self.active=False
			self.save()
			return True
		else:
			self.active=True
			self.save()
			return False



class FallBacks(models.Model):
	feed_name=models.ForeignKey(TheFeed)

	def __unicode__(self):
		return '%s' % self.feed_name








	




