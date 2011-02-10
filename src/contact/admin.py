from django.contrib import admin
from contact.models import Submission

class SubmissionAdmin(admin.ModelAdmin):
    model = Submission
admin.site.register(Submission, SubmissionAdmin)



