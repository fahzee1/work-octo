from django.contrib import admin
from affiliates.models import Affiliate

class AffiliateAdmin(admin.ModelAdmin):
    model = Affiliate
admin.site.register(Affiliate, AffiliateAdmin)
