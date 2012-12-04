from django.contrib import admin
from apps.adspace.models import Campaign, Ad

class CampaignAdmin(admin.ModelAdmin):
    model = Campaign
admin.site.register(Campaign, CampaignAdmin)

class AdAdmin(admin.ModelAdmin):
    model = Ad
    list_display = ('campaign', 'type', 'ad')
    list_filter = ('campaign', 'type')
admin.site.register(Ad, AdAdmin)
