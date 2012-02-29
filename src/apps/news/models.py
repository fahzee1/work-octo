from django.core.urlresolvers import reverse
from django.db import models
from django.template import defaultfilters

class Category(models.Model):
    name = models.CharField(max_length=64)
    brafton_id = models.IntegerField()

    def __unicode__(self):
        return '%s' % self.name

class Article(models.Model):
    brafton_id = models.IntegerField()
    heading = models.CharField(max_length=128)
    content = models.TextField()
    summary = models.TextField()

    image = models.ImageField(upload_to='brafton/',max_length=256, blank=True, null=True)
    image_caption = models.CharField(max_length=128, blank=True, null=True)

    categories = models.ManyToManyField(Category)
    date_created = models.DateTimeField(auto_now_add=True)

    def related(self):
        pass

    def get_absolute_url(self):
        return reverse('news-article', kwargs={
            'article_title': defaultfilters.slugify(self.heading),
            'article_id': self.id,
        })

    def __unicode__(self):
        return '%s - %s' % (self.heading, self.brafton_id)
