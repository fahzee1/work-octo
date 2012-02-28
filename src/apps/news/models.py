from django.db import models

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

    image = models.ImageField(upload_to='brafton/', blank=True, null=True)
    image_caption = models.CharField(max_length=128, blank=True, null=True)

    categories = models.ManyToManyField(Category)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s' % (self.heading, self.brafton_id)
