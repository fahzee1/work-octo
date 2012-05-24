from django.db import models

# Create your models here.
class SpunContent(models.Model):
    url = models.CharField(max_length=256)
    name = models.CharField(max_length=24)
    content = models.CharField(max_length=128)

    def __unicode__(self):
        return '%s - %s' % (self.url, self.name,)

# 5LINX conference 
class LinxContext(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=15)
    rin = models.CharField(max_length=10)

    def __unicode__(self):
        return '%s - %s - %s - %s' % (self.name,
            self.rin, self.phone, self.email)
