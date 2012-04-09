import settings
import os
import re

from django.db import models

class Affiliate(models.Model):
    agent_id = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    use_call_measurement = models.BooleanField(default=False)

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
    state = models.CharField(max_length=128)
    zipcode = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    fax = models.CharField(max_length=128)
    email = models.EmailField()
    website = models.CharField(max_length=128)
    comments = models.TextField()
    status = models.CharField(max_length=10, choices=PROFILE_STATUS,
        default="PENDING")

    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.name
