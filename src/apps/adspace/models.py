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
TYPE_CHOICES = (
    ('hero_banner_backdrop','Hero Banner Backdrop'),
    ('hero_banner','Hero Banner'),
    ('promo_banner','Promo Banner (224x184)'),
    ('promo_banner_full', 'Full Promo Banner (671x184)'),
    ('side_bar','Side Bar Ad (251x286)'),
    ('product_page','Product Page Ad (934x130)'),
    ('mobile_hero', 'Mobile Hero Banner'),
    ('leaderboard', 'Leaderboard (728x90)'),
    ('banner','Banner (468x60)'),
    ('skyscaper','Skyscraper (120x600)'),
    ('wide_skyscraper','Wide Skyscraper (160x600)'),
    ('small_square','Small Square (200x200)'),
    ('square','Square (250x250)'),
    ('medium_rectangle','Medium Rectangle (300x250)'),
    ('large_rectangle','Large Rectangle (336x280)'),
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

    def file_path(instance, filename):
        if not instance.campaign:
            return os.path.join('banner_images', 'unfiled', filename)
        return os.path.join('banner_images',
            'campaign_%s' % instance.campaign.id, filename)

    campaign = models.ForeignKey(Campaign)
    type = models.CharField(max_length=48, choices=TYPE_CHOICES)
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
        return '%s - %s : %s' % (self.campaign.name, self.type, self.sub_id)

    def get_active_campaign(self):
        today = datetime.date.today()
        weekday = datetime.date.today().weekday()
        campaigns = Campaign.objects.filter(Q(start_date__lte=today) | Q(start_date__isnull=True)).filter(
            Q(end_date__gte=today) | Q(end_date__isnull=True)).order_by('-pk')

        for campaign in campaigns:
            try:
                if campaign.__getattribute__(WEEKDAYS[weekday]):
                    return Ad.objects.filter(
                        campaign=campaign, type=self.type).order_by(
                        'date_created')[0]
            except Ad.DoesNotExist:
                pass

        raise Ad.DoesNotExist
