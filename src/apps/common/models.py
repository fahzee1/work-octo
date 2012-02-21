from django.db import models

# Create your models here.
class SpunContent(models.Model):
    url = models.CharField(max_length=256)
    name = models.CharField(max_length=24)
    content = models.CharField(max_length=128)

    def __unicode__(self):
        return '%s - %s' % (self.url, self.name,)
