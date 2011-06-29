from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=12)
    upfront = models.CharField(max_length=10)
    adt_upfront = models.CharField(max_length=10)

    standard_monitoring = models.CharField(max_length=6)
    landline_monitoring = models.CharField(max_length=6)
    broadband_monitoring = models.CharField(max_length=6)
    cellular_monitoring = models.CharField(max_length=6)
    cellular_interactive_monitoring = models.CharField(max_length=6)

    
    def __unicode__(self):
        return self.name
