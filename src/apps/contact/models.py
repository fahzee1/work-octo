from django.db import models
from django.contrib.localflavor.us.models import (PhoneNumberField, 
    USStateField)


# Create your models here.

class Submission(models.Model):

    DEPARTMENT_CHOICES = (
        ('customer_service', 'Customer Service'),
        ('sales', 'Sales'),
        ('careers', 'Carriers'),
    )
    
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    phone = PhoneNumberField()
    city = models.CharField(max_length=32, blank=True, null=True)
    state = USStateField(blank=True, null=True)
    package = models.CharField(max_length=24, blank=True, null=True)
    feedback_type = models.CharField(max_length=32, blank=True, null=True)

    department = models.CharField(max_length=32,
                                  blank=True, null=True,
                                  choices=DEPARTMENT_CHOICES)

    rep_name = models.CharField(max_length=128, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    
    def get_first_name(self):
        return self.name.split(' ')[0]


    def get_last_name(self):
        return self.name.split(' ')[-1]


    def __unicode__(self):
        return '%s : %s' % (self.name, self.phone,)
