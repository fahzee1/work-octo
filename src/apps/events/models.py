from datetime import datetime, timedelta

from django.db import models
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your models here.
class Venue(models.Model):

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    image = models.ImageField(upload_to="venue", blank=True)

    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('venue_page', kwargs={
            'city': self.city.lower().replace(' ', '-'),
            'state': self.state.lower().replace(' ', '-'),
            'venue': self.name.lower().replace(' ', '-'),
            'venue_id': self.id,
        })

class Event(models.Model):
    title = models.CharField(max_length=256)
    venue = models.ForeignKey(Venue)
    description = models.TextField(blank=True)
    event_url = models.CharField(max_length=500, blank=True, default=u"")
    eventdate = models.DateField(blank=True)
    eventstart = models.TimeField(blank=True, null=True)
    eventfinish = models.TimeField(blank=True, null=True)
    image = models.ImageField(upload_to="event", blank=True)

    def __unicode__(self):
        return self.title

    def get_event_url(self):
        return reverse('event_page', kwargs={
            'city': self.venue.city.lower().replace(' ', '-'),
            'state': self.venue.state.lower().replace(' ', '-'),
            'venue': self.venue.name.lower().replace(' ', '-'),
            'venue_id': self.venue.id,
            'event_title': self.title.lower().replace(' ', '-'),
            'event_id': self.id,
        })        

    class Meta:
        ordering = ['eventdate', 'eventstart']