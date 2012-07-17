import settings
import os
import re

from django.db import models
from django.core.mail import send_mail
from django.template import loader, Context
from django.contrib.localflavor.us.us_states import STATE_CHOICES

class Affiliate(models.Model):
    agent_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    use_call_measurement = models.BooleanField(default=False)
    homesite_override = models.BooleanField(default=False,
        help_text='Check this if the affiliate should be under the HOMESITE agent_id')
    pixels = models.TextField(blank=True, null=True,
        help_text='Add HTML here for affiliate Pixels')
    thank_you = models.CharField(max_length=128,blank=True, null=True,
        help_text='If the affiliate has a custom thank you page ender the URL after /thank-you here')
    conversion_pixels = models.TextField(blank=True, null=True,
        help_text='Add HTML here for affiliate conversion Pixels')

    def has_landing_page(self):
        try:
            lp = LandingPage.objects.get(affiliate=self)
            return True
        except:
            pass
        return False

    def add_landing_page(self):
        if self.has_landing_page():
            return False
        lp = LandingPage()
        temp = AffTemplate.objects.get(folder='coreg')
        lp.template = temp
        lp.affiliate = self
        lp.save()
        return True

    def remove_landing_page(self):
        try:
            lp = LandingPage.objects.get(affiliate=self)
            lp.delete()
            return True
        except:
            pass
        return False

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.agent_id)


class AffTemplate(models.Model):

    root_file = os.path.join(settings.PROJECT_ROOT, 'src', 'templates', 'affiliates')
    name = models.CharField(max_length=32, unique=True)
    # this is the directory that is in 
    # the 'src/templates/affiliates' directory
    folder = models.CharField(max_length=32, unique=True)
    
    @property
    def filepath(self):
        return os.path.join(self.root_file, self.folder)

    def get_templates(self):
        try:
            tmpl = []
            for item in os.listdir(self.filepath):
                m = re.match(r'(.+)\.html', item)
                if m is not None:
                    tmpl.append(m.group())
            return tmpl
        except OSError:
            return []

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.folder)


class LandingPage(models.Model):
    affiliate = models.ForeignKey(Affiliate)
    template = models.ForeignKey(AffTemplate)

    def get_filename(self, page_name):
        import imp

        f, filename, desc = imp.find_module('settings', [self.template.filepath])
        project = imp.load_module('a40bd22344', f, filename, desc)
                
        for page in project.TEMPLATE_PAGES:
            if page_name == page[0]:
                return page[1]

        return None
    def __unicode__(self):
        return '%s - %s' % (self.affiliate, self.template)


class Profile(models.Model):

    PROFILE_STATUS = (
        ('DECLINED', 'Declined'),
        ('APPROVED', 'Approved'),
        ('PENDING', 'Pending')
    )

    name = models.CharField(max_length=128)
    title = models.CharField(max_length=128, blank=True, null=True)
    company_name = models.CharField(max_length=128)
    taxid = models.CharField(max_length=12)
    street_address = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    fax = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField()
    website = models.CharField(max_length=128)
    comments = models.TextField(help_text='Please include background information about your company and how you feel that we can work together to achieve mutual success through our affiliate program.')
    status = models.CharField(max_length=10, choices=PROFILE_STATUS,
        default="PENDING")

    agreed_to_terms = models.BooleanField(default=False)
    sign = models.CharField(max_length=200)
    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)

    class Meta:
        verbose_name = 'Affiliate Request'
        verbose_name_plural = 'Affiliate Requests'

    def send_signup_to_bizdev(self):
        subject = 'Protect America Affiliate Program'
        t = loader.get_template('emails/new_affiliate_signup.html')
        c = Context({
            'name': self.name,
            'title': self.title,
            'company_name': self.company_name,
            'website': self.website,
            'phone': self.phone,
            'fax': self.fax,
            'email': self.email,
            'taxid': self.taxid,
            'street_address': self.street_address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'comments': self.comments,
        })
        send_mail(subject, t.render(c), '"Protect America" <noreply@protectamerica.com>',
            ['BusinessDevelopment@protectamerica.com'], fail_silently=True)

    def __unicode__(self):
        return '%s' % self.name
