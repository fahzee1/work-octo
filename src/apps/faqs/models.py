from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField

class Question(models.Model):
    question = models.TextField()
    answer = models.TextField()

    expert_question = models.BooleanField(
        help_text="Show this question on HomeSecurityExpert")
    active = models.BooleanField(
        help_text="Display on website")
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.question

class Tip(models.Model):

    tip = models.TextField()

    expert_question = models.BooleanField(
        help_text="Show this question on HomeSecurityExpert")
    active = models.BooleanField(
        help_text="Display on website")
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tip

class QuestionSubmission(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    phone = PhoneNumberField()

    def __unicode__(self):
        return self.name