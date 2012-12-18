from django.db import models
from django.conf import settings
import os
import datetime
from django.db.models import Q
from django.http import HttpResponse

WEEKDAYS = (
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',
)

class Campaign(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % (self.name,)

    def save(self, *args, **kwargs):
            filepath = '%s/adspace/%s/' % (
                settings.TEMPLATE_DIRS[0], self.name,)
            if not os.path.isdir(filepath):
                os.mkdir(filepath)
            super(Campaign, self).save(*args, **kwargs)

class AdSpot(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)

    def __unicode__(self):
        return '%s' % (self.name,)

class Ad(models.Model):

    def file_path(instance, filename):
        if not instance.campaign:
            return os.path.join('banner_images', 'unfiled', filename)
        return os.path.join('banner_images',
            'campaign_%s' % instance.campaign.id, filename)

    campaign = models.ForeignKey(Campaign)
    type = models.ForeignKey(AdSpot)
    sub_id = models.CharField(max_length=128, blank=True, null=True)
    ad = models.ImageField(upload_to=file_path)

    alt = models.CharField(max_length=128, blank=True, null=True)
    element_id = models.CharField(max_length=128, blank=True, null=True,
        help_text='The ID of the image element for styling')
    url = models.CharField(max_length=128, blank=True, null=True)
    width = models.CharField(max_length=4, blank=True, null=True)
    height = models.CharField(max_length=4, blank=True, null=True)
    inline_styles = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s' % (self.campaign.name, self.type.name)
