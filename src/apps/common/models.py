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

class BlackFriday(models.Model):
    email = models.EmailField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email


class AbTestCode(models.Model):
    name = models.CharField(max_length=255)
    aff_id = models.CharField(max_length=255,help_text='Agent id to be associated with this test')
    code = models.TextField(help_text='Html code used in this A/B test')

    def __unicode__(self):
        return self.name

class AbTest(models.Model):
    name = models.CharField(max_length=255)
    code_choices = models.ManyToManyField(AbTestCode,related_name='abtest')

    def __unicode__(self):
        return self.name

