from django.contrib import admin
from apps.contact.models import Submission

class SubmissionAdmin(admin.ModelAdmin):
    model = Submission
admin.site.register(Submission, SubmissionAdmin)



