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

class Ad(models.Model):
    TYPE_CHOICES = (
        ('hero-banner-backdrop','Hero Banner Backdrop'),
        ('hero-banner','Hero Banner'),
        ('promo-banner','Promo Banner'),
        ('side-bar','Side Bar Ad'),
        ('product-page','Product Page Ad'),
    )

    def file_path(instance, filename):
        if not instance.campaign:
            return os.path.join('banner_images', 'unfiled', filename)
        return os.path.join('banner_images',
            'campaign_%s' % instance.campaign.id, filename)

    campaign = models.ForeignKey(Campaign)
    type = models.CharField(max_length=48, choices=TYPE_CHOICES)
    sub_id = models.CharField(max_length=128, blank=True, null=True)
    ad = models.ImageField(upload_to=file_path)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s : %s' % (self.campaign.name, self.type, self.sub_id)

    def get_active_campaign(self):
        today = datetime.date.today()
        weekday = datetime.date.today().weekday()
        campaigns = Campaign.objects.filter(Q(start_date__lte=today) | Q(start_date__isnull=True)).filter(
            Q(end_date__gte=today) | Q(end_date__isnull=True)).order_by('-pk')

        for campaign in campaigns:
            try:
                if campaign.__getattribute__(WEEKDAYS[weekday]):
                    return Ad.objects.get(campaign=campaign, type=self.type)
            except Ad.DoesNotExist:
                pass

        raise Ad.DoesNotExist
