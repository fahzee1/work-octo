from django.db import models

class Affiliate(models.Model):
    agent_id = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    use_call_measurement = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % (self.name,)
