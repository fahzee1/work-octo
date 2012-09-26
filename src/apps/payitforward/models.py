from django.db import models
from colorful.fields import RGBColorField

class Organization(models.Model):
    name = models.CharField(max_length=64)
    color = RGBColorField()
    image = models.ImageField(upload_to='payitforward/')

    def points(self):
        total = 0
        for ps in self.points_set.all():
            total = total + int(ps.value)
        return total

    def __unicode__(self):
        return '%s' % self.name

class Points(models.Model):
    POINT_TYPES = (
        ('revenue', 'Revenue'),
        ('awareness', 'Awareness')
    )
    type = models.CharField(max_length=10, choices=POINT_TYPES)
    value = models.CharField(max_length=6)
    organization = models.ForeignKey(Organization)

    def __unicode__(self):
        return '%s points awarded to %s for %s' % (self.value,
            self.organization, self.type)