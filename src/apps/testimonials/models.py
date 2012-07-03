from django.db import models
from django.contrib.localflavor.us.models import (PhoneNumberField, 
    USStateField)
from django.template import loader, Context
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage

class Testimonial(models.Model):

    EXPERIENCE_CHOICES = (
        ('POSITIVE', 'Positive Feedback'),
        ('NEGATIVE', 'Negative Feedback'),
        ('SUGGESTION', 'General Suggestion'),
        ('ISSUE', 'Unresolved Issue'),
        ('OTHER', 'Other'),
    )
    DEPARTMENT_CHOICES = (
        ('BILLING', 'Billing'),
        ('INSTALL', 'Customer Installation'),
        ('SERVICE', 'Customer Service'),
        ('MONITORING', 'Monitoring Station'),
        ('AGREEMENT', 'Monitoring Agreement'),
        ('OTHER', 'Other/Unknown'),
        ('SALES', 'Sales'),
    )

    first_name = models.CharField(max_length=36)
    last_name = models.CharField(max_length=36, blank=True, null=True)
    city = models.CharField(max_length=24)
    state = models.CharField(max_length=24)
    email = models.EmailField(blank=True, null=True)
    

    experience = models.CharField(max_length=10,
        choices=EXPERIENCE_CHOICES,
        blank=True, null=True)
    department = models.CharField(max_length=10,
        choices=DEPARTMENT_CHOICES,
        blank=True, null=True)
    rep = models.CharField(max_length=64, blank=True, null=True)

    can_post = models.BooleanField(default=False,
        help_text='I agree to allow Protect America to post this feedback publicly.')

    testimonial = models.TextField()

    display = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('single-testimonial', kwargs={'testimonial_id': self.id})

    def __unicode__(self):
        return '%s %s on %s' % (self.first_name,
            self.last_name, self.date_created)

class Textimonial(models.Model):
    first_name = models.CharField(max_length=36)
    last_name = models.CharField(max_length=36)
    city = models.CharField(max_length=24)
    state = USStateField(max_length=24)
    email = models.EmailField()
    rating = models.CharField(max_length=4)
    message = models.TextField()
    permission_to_post = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def email_company(self):
        t = loader.get_template('emails/testimonial_to_company.html')
        c = Context({'sub': self})
        email = EmailMessage(
            'Testimonial Submission',
            t.render(c),
            '"Protect America" <noreply@protectamerica.com>',
            ['feedback@protectamerica.com'],
            ['robert@protectamerica.com'],
             headers = {'Reply-To': 'noreply@protectamerica.com'})
        email.send()

    def get_absolute_url(self):
        return reverse('single-testimonial', kwargs={'testimonial_id': self.id})

class Vidimonial(models.Model):
    video_url = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('video-testimonial', kwargs={'testimonial_id': self.id})