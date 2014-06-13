from django.contrib import admin
from apps.affiliates.models import Affiliate, AffTemplate, LandingPage, Profile

class AffiliateAdmin(admin.ModelAdmin):
    model = Affiliate
    search_fields=['agent_id','name','phone']
admin.site.register(Affiliate, AffiliateAdmin)

class AffTemplateAdmin(admin.ModelAdmin):
    model = AffTemplate
admin.site.register(AffTemplate, AffTemplateAdmin)

class LandingPageAdmin(admin.ModelAdmin):
    model = LandingPage
    list_filter = ['affiliate',]
    raw_id_fields = ('affiliate',)

admin.site.register(LandingPage, LandingPageAdmin)

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
admin.site.register(Profile, ProfileAdmin)
