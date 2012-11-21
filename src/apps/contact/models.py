from datetime import datetime

from django.db import models
from django.contrib.localflavor.us.models import (PhoneNumberField, 
    USStateField)
from django.template import loader, Context
from django.core.mail import EmailMessage

# Create your models here.
DEPARTMENT_CHOICES = (
    ('billing', 'Billing'),
    ('customer_installations', 'Customer Installations'),
    ('customer_service', 'Customer Service'),
    ('monitoring_station', 'Monitoring Station'),
    ('monitoring_agreement', 'Monitoring Agreement'),
    ('other', 'Other'),
    ('sales', 'Sales'), 
)

FEEDBACK_CHOICES = (
    ('general', 'General Feedback'),
    ('positive', 'Positive Feedback'),
    ('negative', 'Negative Feedback'),
    ('other', 'Other'),
)

class Submission(models.Model):

    HOMEOWNER_CHOICES = (
        ('YES', 'Yes'),
        ('NO', 'No'),
    )

    CREDITRATING_CHOICES = (
        ('EXCELLENT', 'Excellent (720 or above)'),
        ('GOOD', 'Good (660 - 719)'),
        ('AVERAGE', 'Average (620 - 659)'),
        ('BELOW_AVERAGE', 'Below Average (580 - 619)'),
        ('POOR', 'Poor (579 or Below)'),
    )
    
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    phone = PhoneNumberField()
    city = models.CharField(max_length=32, blank=True, null=True)
    state = USStateField(blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=12, blank=True, null=True)
    package = models.CharField(max_length=24, blank=True, null=True)
    feedback_type = models.CharField(max_length=32, blank=True, null=True)

    department = models.CharField(max_length=32,
                                  blank=True, null=True,
                                  choices=DEPARTMENT_CHOICES)

    rep_name = models.CharField(max_length=128, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    homeowner = models.CharField(max_length=3, blank=True, null=True,
        choices=HOMEOWNER_CHOICES)
    creditrating = models.CharField(max_length=15, blank=True, null=True,
        choices=CREDITRATING_CHOICES)

    consent = models.BooleanField(default=False, help_text="By checking this box, I expressly give consent to be contacted according to the Terms and Conditions")

    referer_page = models.CharField(max_length=256, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)

    
    def get_first_name(self):
        return self.name.split(' ')[0]

    def get_last_name(self):
        return self.name.split(' ')[-1]

    def __unicode__(self):
        return '%s : %s' % (self.name, self.phone,)

class GoogleExperiment(models.Model):
    google_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s : %s' % (self.google_id, self.name,)

class Lead(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    phone = PhoneNumberField()

    agent_id = models.CharField(max_length=24, blank=True, null=True)
    source = models.CharField(max_length=64, blank=True, null=True)
    affkey = models.CharField(max_length=64, blank=True, null=True)

    search_engine = models.CharField(max_length=128, blank=True, null=True)
    search_keywords = models.CharField(max_length=128, blank=True, null=True)

    referer_page = models.CharField(max_length=256, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s | %s - %s : %s %s' % (self.id,
            self.agent_id, self.source, self.name, self.phone)

class EcomLead(Lead):
    city = models.CharField(max_length=32)
    state = USStateField()
    address = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=12)
    consent = models.BooleanField(default=False)

class ContactUs(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    phone = PhoneNumberField()
    department = models.CharField(max_length=32, choices=DEPARTMENT_CHOICES)
    message = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)

    def email_company(self):
        t = loader.get_template('emails/contact_us_to_company.html')
        c = Context({'sub': self})
        email = EmailMessage(
            'Contact Form Submission',
            t.render(c),
            '"Protect America" <noreply@protectamerica.com>',
            ['careops@protectamerica.com'],
            ['"Robert Johnson" <robert@protectamerica.com>'],
             headers = {'Reply-To': 'noreply@protectamerica.com'})
        email.send()

    def __unicode__(self):
        return '%s : %s' % (self.name, self.phone,)

class MovingKit(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)

    current_phone = PhoneNumberField()
    current_city = models.CharField(max_length=32)
    current_state = USStateField()
    current_address = models.CharField(max_length=128)
    current_zipcode = models.CharField(max_length=12)

    new_phone = PhoneNumberField(blank=True, null=True)
    new_city = models.CharField(max_length=32, blank=True, null=True)
    new_state = USStateField(blank=True, null=True)
    new_address = models.CharField(max_length=128, blank=True, null=True)
    new_zipcode = models.CharField(max_length=12, blank=True, null=True)

    send_to_current_address = models.BooleanField(default=True)
    shipping_city = models.CharField(max_length=32, blank=True, null=True)
    shipping_state = USStateField(blank=True, null=True)
    shipping_address = models.CharField(max_length=128, blank=True, null=True)
    shipping_zipcode = models.CharField(max_length=12, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def email_company(self):
        t = loader.get_template('emails/moving_kit_to_company.html')
        c = Context({'sub': self})
        email = EmailMessage(
            'New Moving Kit Request',
            t.render(c),
            '"Protect America" <noreply@protectamerica.com>',
            ['shipping@protectamerica.com'],
            ['"Robert Johnson" <robert@protectamerica.com>'],
             headers = {'Reply-To': 'noreply@protectamerica.com'})
        email.send()

    def __unicode__(self):
        return '%s : %s' % (self.name, self.current_phone,)

class CEOFeedback(models.Model):

    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    phone = PhoneNumberField()
    city = models.CharField(max_length=32, blank=True, null=True)
    state = USStateField(blank=True, null=True)
    feedback_type = models.CharField(max_length=32, choices=FEEDBACK_CHOICES)

    department = models.CharField(max_length=32, choices=DEPARTMENT_CHOICES)
    rep_name = models.CharField(max_length=128, blank=True, null=True)
    message = models.TextField()

    rating = models.CharField(max_length=4, default='0')
    converted = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_read = models.DateTimeField(null=True, blank=True)

    def email_company(self):
        t = loader.get_template('emails/ceo_feedback_to_company.html')
        c = Context({'sub': self})
        email = EmailMessage(
            'CEO Feedback: %s' % self.feedback_type,
            t.render(c),
            '"Protect America" <noreply@protectamerica.com>',
            ['feedback@protectamerica.com'],
            ['"Robert Johnson" <robert@protectamerica.com>'],
             headers = {'Reply-To': 'noreply@protectamerica.com'})
        email.send()

    def convert_to_textimonial(self):
        from apps.testimonials.models import Textimonial

        t = Textimonial()
        names = self.name.split(' ')
        if len(names) > 1:
            t.first_name = names[0]
            t.last_name = names[-1]
        else:
            t.first_name = names[0]
            t.last_name = ''

        t.city = self.city
        t.state = self.state
        t.email = self.email
        t.rating = self.rating
        t.message = self.message
        t.permission_to_post = True
        t.display = True
        t.save()

        t.date_read = self.date_read
        t.converted_from = self
        t.save()

        self.converted = True
        self.save()


    def mark_as_read(self):
        if self.date_read:
            return
    
        self.date_read = datetime.now()
        self.save()
        return True


    def __unicode__(self):
        return '%s : %s - %s' % (self.name, self.phone, self.feedback_type)

class TellAFriend(models.Model):

    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)

    friend_name = models.CharField(max_length=128)
    friend_email = models.EmailField(max_length=128)

    date_created = models.DateTimeField(auto_now_add=True)

    def email_friend(self):
        t = loader.get_template('emails/tell_a_friend.html')
        c = Context({'sub': self})
        email = EmailMessage(
            'Info About Our Neighborhood Security',
            t.render(c),
            '"%s" <noreply@protectamerica.com>' % self.name,
            [self.friend_email],
            ['"Protect America" <noreply@protectamerica.com>'],
             headers = {'Reply-To': 'noreply@protectamerica.com'})
        email.send()
        
    def __unicode__(self):
        return '%s -> %s' % (self.name, self.friend_name,)

class DoNotCall(models.Model):

    name = models.CharField(max_length=128)
    phone = PhoneNumberField()

    date_created = models.DateTimeField(auto_now_add=True)

    def email_company(self):
        t = loader.get_template('emails/do-not-call.html')
        c = Context({'sub': self})
        email = EmailMessage(
            'New Do Not Call Request',
            t.render(c),
            '"Protect America" <noreply@protectamerica.com>',
            ['donotcall@protectamerica.com'],
            ['"Robert Johnson" <robert@protectamerica.com>'],
             headers = {'Reply-To': 'noreply@protectamerica.com'})
        email.send()

    def __unicode__(self):
        return '%s : %s' % (self.name, self.phone,)

class PayItForward(models.Model):

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128)
    comments = models.TextField()

    def email_shawne(self):
        t = loader.get_template('emails/pay_it_forward.html')
        c = Context({'sub': self})
        email = EmailMessage(
            'New Pay It Forward Submission',
            t.render(c),
            '"Protect America" <noreply@protectamerica.com>',
            ['adrian@protectamerica.com', 'robert@protectamerica.com'],
            ['"Protect America" <noreply@protectamerica.com>'])
        email.send()

    def __unicode__(self):
        return '%s %s - %s' % (self.first_name, self.last_name, self.email)
