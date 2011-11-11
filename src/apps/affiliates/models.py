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
        return '%s' % (self.name,)


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
