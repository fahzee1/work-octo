from django.contrib import admin
from apps.contact.models import Submission, ContactUs, MovingKit, CEOFeedback, TellAFriend, GoogleExperiment, Lead

class SubmissionAdmin(admin.ModelAdmin):
    model = Submission
    search_fields = ['id', 'phone', 'email']
admin.site.register(Submission, SubmissionAdmin)

class ContactUsAdmin(admin.ModelAdmin):
    model = ContactUs
admin.site.register(ContactUs, ContactUsAdmin)

class MovingKitAdmin(admin.ModelAdmin):
    model = MovingKit
admin.site.register(MovingKit, MovingKitAdmin)

class CEOFeedbackAdmin(admin.ModelAdmin):
    model = CEOFeedback
admin.site.register(CEOFeedback, CEOFeedbackAdmin)

class TellAFriendAdmin(admin.ModelAdmin):
    model = TellAFriend
admin.site.register(TellAFriend, TellAFriendAdmin)

class GoogleExperimentAdmin(admin.ModelAdmin):
    model = GoogleExperiment
admin.site.register(GoogleExperiment, GoogleExperimentAdmin)

class LeadAdmin(admin.ModelAdmin):
    model = Lead
    list_filter = ('agent_id',)
    search_fields = ['id', 'agent_id', 'phone', 'email', 'search_keywords']
admin.site.register(Lead, LeadAdmin)