from django.contrib import admin
from apps.affiliates.models import Affiliate, AffTemplate, LandingPage

class AffiliateAdmin(admin.ModelAdmin):
    model = Affiliate
admin.site.register(Affiliate, AffiliateAdmin)

class AffTemplateAdmin(admin.ModelAdmin):
    model = AffTemplate
admin.site.register(AffTemplate, AffTemplateAdmin)

class LandingPageAdmin(admin.ModelAdmin):
    model = LandingPage
admin.site.register(LandingPage, LandingPageAdmin)
