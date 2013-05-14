import os

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

class Email(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    html = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('emails:render_email', kwargs={
            'email_slug': self.slug,
            'email_id': self.id,
            })

    def save(self, *args, **kwargs):
        super(Email, self).save(*args, **kwargs)
        
        filepath = os.path.join(settings.MEDIA_ROOT, 'email_images')
        if self.id:
            filepath = os.path.join(filepath, 'email_' + str(self.id))
        else:
            filepath = os.path.join(filepath, 'unfiled')

        # create a folder in the media/uploads with the id of the model
        if not os.path.exists(filepath):
            os.mkdir(filepath)

class EmailImage(models.Model):

    def file_path(instance, filename):
        if not instance.email:
            return os.path.join('email_images', 'unfiled')
        return os.path.join('email_images',
            'email_%s' % instance.email.id, filename)

    email = models.ForeignKey(Email)
    image = models.ImageField(upload_to=file_path)

    date_created = models.DateTimeField(auto_now_add=True)