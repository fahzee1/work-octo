import os
import hashlib

from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=12)
    upfront = models.CharField(max_length=10)

    adt_upfront = models.CharField(max_length=10)
    adt_monitoring = models.CharField(max_length=6, blank=True, null=True)

    standard_monitoring = models.CharField(max_length=6)
    landline_monitoring = models.CharField(max_length=6)
    broadband_monitoring = models.CharField(max_length=6)
    cellular_monitoring = models.CharField(max_length=6)
    cellular_interactive_monitoring = models.CharField(max_length=6)

    
    def __unicode__(self):
        return self.name

class PackageCode(models.Model):
    code = models.CharField(max_length=10)
    cart = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        random_data = os.urandom(128)
        tcode = hashlib.md5(random_data).hexdigest()[:5]
        if PackageCode.objects.filter(code=tcode):
            self.generate_code()
        self.code = tcode
        return tcode

    def __unicode__(self):
        return self.code