from django.db import models

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