from datetime import datetime
from django.db import models
from django.contrib.localflavor.us.models import (PhoneNumberField,
    USStateField)
from django.template import loader, Context
from django.core.mail import EmailMessage
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

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
    email = models.EmailField(default='',max_length=128,blank=True,null=True)
    phone = PhoneNumberField()

    agent_id = models.CharField(max_length=24, blank=True, null=True)
    source = models.CharField(max_length=64, blank=True, null=True)
    affkey = models.CharField(max_length=64, blank=True, null=True)
    gclid = models.CharField(max_length=255, blank=True, null=True)

    search_engine = models.CharField(max_length=128, blank=True, null=True)
    search_keywords = models.CharField(max_length=128, blank=True, null=True)

    referer_page = models.CharField(max_length=256, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    lc_url = models.CharField(max_length=256, blank=True, null=True, help_text='Url of Lead Conduit Submission')
    lc_id = models.CharField(max_length=256, blank=True, null=True, help_text='Lead Conduit lead id')
    lc_error = models.BooleanField(default=False,blank=True, help_text='Was there a error with the Lead Conduit submission?')
    lc_reason = models.CharField(max_length=256, blank=True, null=True, help_text='Lead Conduit reason for not submitting if one')

    device = models.CharField(max_length=256, blank=True, null=True, help_text='Type of device used')
    operating_system = models.CharField(max_length=256, blank=True, null=True, help_text='Type of operating system used')
    browser = models.CharField(max_length=256, blank=True, null=True, help_text='Type of browser used')

    form_values = models.TextField(default='',blank=True,null=True)
    trusted_url = models.CharField(max_length=256, blank=True, null=True, help_text='Trusted Url grabbed from homepage javascript')
    ip_address = models.CharField(max_length=256, blank=True, null=True)
    retry = models.BooleanField(default=False,blank=True,help_text="Lead needs to be resent to Lead Conduit")
    number_of_retries = models.IntegerField(default=0,blank=True)
    call_me = models.CharField(max_length=200, blank=True, null=True)
    retry_call_me = models.BooleanField(default=False,blank=True,help_text="Retry based on call_me")

    class Meta:
        ordering = ['-date_created']


    def __unicode__(self):
        return '%s | %s - %s : %s %s' % (self.id,
            self.agent_id, self.source, self.name, self.phone)


    def call_now(self):
        """
        Check if its a good time to add to lead tracking based
        on call_me on lead model. (morning, afternoon, evening)
        """

        evening = [19] #7pm
        morning = [9,10,11,12] #9am,10am,11am,12pm

        weekday = [1,2,3,4,5]
        saturday = [6]
        sunday = [7]

        day = datetime.now().isoweekday()
        if day in weekday:
            evening.extend((20,21,22)) #add 8pm,9pm,10pm,10:59pm

        elif day in saturday:
            #evening.append(20) #add 8pm

        elif day in sunday:
            morning = [11] #open at 11am
            evening.append(20) #add 8pm-8:59pm



        time_chart = {
                    'morning':morning,
                    'afternoon':[13,14,15,16,17,18], #1pm,3pm,4pm,5pm,6pm
                    'evening':evening
        }

        if not self.call_me:
            return True

        pa_open = None
        timeofday = None
        hour = datetime.now().time().hour

        for time in time_chart:
            if hour in time_chart[time]:
                pa_open = True
                timeofday = time
                break

        if pa_open:
            if self.call_me == timeofday:
                if self.retry_call_me:
                    self.retry_call_me = False
                    self.save()
                return True

            else:
                if not self.retry_call_me:
                    self.retry_call_me = True
                    self.save()
                return False

        else:
            if not self.retry_call_me:
                self.retry_call_me = True
                self.save()
            return False






class EcomLead(Lead):
    city = models.CharField(max_length=32, blank=True, null=True)
    state = USStateField(blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    address_2 = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=12, blank=True, null=True)
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
        from_email = 'Protect America <noreply@protectamerica.com>'
        to_email = 'chat@protectamerica.com'
        try:
            send_mail('Contact Form Submission',
                      t.render(c),
                      from_email,
                      [to_email],fail_silently=False)
        except:
            print 'error sending contact us email'


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
    read = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_read = models.DateTimeField(null=True, blank=True)

    ip_address = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        ordering = ['-date_created']



    def sanitized_name(self):
        import re
        cleaned_name = re.sub(r'\W+','',self.name)
        return cleaned_name


    def email_company(self,data):
        subject = 'CEO Feedback: %s : %s' % (self.feedback_type,self.sanitized_name())
        from_email = 'Protect America <noreply@protectamerica.com>'
        to_email = 'feedback@protectamerica.com'
        data['sub'] = self
        html_content = render_to_string('emails/ceo_feedback_to_company.html',data)
        try:
            msg = EmailMultiAlternatives(subject,html_content,from_email,[to_email])
            msg.attach_alternative(html_content,'text/html')
            msg.send()
        except:
            subject = 'CEO Feedback email failed sending to feedback@protectamerica.com'
            to_email = 'Development <Development@protectamerica.com>'
            msg = EmailMultiAlternatives(subject,html_content,from_email,[to_email])
            msg.attach_alternative(html_content,'text/html')
            msg.send()


    """
    def email_company(self,data):
        t = loader.get_template('emails/ceo_feedback_to_company.html')
        c = Context({'sub': self})
        email = EmailMessage(
            'CEO Feedback: %s' % self.feedback_type,
            t.render(c),
            '"Protect America" <noreply@protectamerica.com>',
            ['feedback@protectamerica.com'],
             headers = {'Reply-To': 'noreply@protectamerica.com'})
        email.send()

    """

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
        self.read = True
        self.save()
        return True

    def remove_duplicate_state(self):
        if self.city and 'Washington, DC' not in self.city:
            name = self.city.split(',')
            self.city = name[0]
            self.save()
            print self.city
        elif self.city and 'Washington, DC' in self.city:
            name = self.city.split(',')
            self.city = name[0]
            self.state = 'DC'
            self.save()
            print self.city,self.state
        else:
            print self.city
            print 'no city or its Washington'



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
