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

    agent_id = models.CharField(max_length=24)
    source = models.CharField(max_length=64)
    affkey = models.CharField(max_length=64)

    referer_page = models.CharField(max_length=256, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s : %s %s' % (self.agent_id, self.source, self.name, self.phone)

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
            ['feedback@protectamerica.com'],
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

    date_created = models.DateTimeField(auto_now_add=True)

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
            ['"Robert Johnson" <robert@protectamerica.com>'],
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