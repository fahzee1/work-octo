from django.db import models

class Testimonial(models.Model):

    EXPERIENCE_CHOICES = (
        ('POSITIVE', 'Positive Feedback'),
        ('NEGATIVE', 'Negative Feedback'),
        ('SUGGESTION', 'General Suggestion'),
        ('ISSUE', 'Unresolved Issue'),
        ('OTHER', 'Other'),
    )
    DEPARTMENT_CHOICES = (
        ('BILLING', 'Billing'),
        ('INSTALL', 'Customer Installation'),
        ('SERVICE', 'Customer Service'),
        ('MONITORING', 'Monitoring Station'),
        ('AGREEMENT', 'Monitoring Agreement'),
        ('OTHER', 'Other/Unkown'),
        ('SALES', 'Sales'),
    )

    first_name = models.CharField(max_length=36)
    last_name = models.CharField(max_length=36, blank=True, null=True)
    city = models.CharField(max_length=24)
    state = models.CharField(max_length=24)
    email = models.EmailField(blank=True, null=True)
    

    experience = models.CharField(max_length=10,
        choices=EXPERIENCE_CHOICES,
        blank=True, null=True)
    department = models.CharField(max_length=10,
        choices=DEPARTMENT_CHOICES,
        blank=True, null=True)
    rep = models.CharField(max_length=64, blank=True, null=True)

    can_post = models.BooleanField(default=False,
        help_text='I agree to allow Protect America to post this feedback publicly.')

    testimonial = models.TextField()

    display = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s %s on %s' % (self.first_name,
            self.last_name, self.date_created)
