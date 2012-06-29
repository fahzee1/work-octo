from django.db import models

class Question(models.Model):

    ANSWER_SETS = (
        ('BOOLEAN', 'Yes / No'),
        ('RATE', 'Rate 1 - 10'),
    )
    
    question = models.CharField(max_length=128)
    answer = models.CharField(max_length=16, choices=ANSWER_SETS)

    def __unicode__(self):
        return '%s - %s' % (self.pk, self.question)

class QuestionSet(models.Model):
    
    name = models.CharField(max_length=64)

    @property
    def question_set(self):
        return QuestionToQuestionSet.objects.filter(
            question_set=self).order_by('-order')

    def __unicode__(self):
        return '%s' % self.name

class QuestionToQuestionSet(models.Model):
    question_set = models.ForeignKey(QuestionSet)
    question = models.ForeignKey(Question)
    order = models.IntegerField()

class Survey(models.Model):
    name = models.CharField(max_length=64)

    @property
    def question_sets(self):
        return QuestionSetToSurvey.objects.filter(
            survey=self).order_by('-order')

    def __unicode__(self):
        return '%s' % self.name

class QuestionSetToSurvey(models.Model):
    survey = models.ForeignKey(Survey)
    question_set = models.ForeignKey(QuestionSet)
    order = models.IntegerField()

class AnsweredQuestion(models.Model):
    survey = models.ForeignKey(Survey)
    question_set = models.ForeignKey(QuestionSet)
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=128)
