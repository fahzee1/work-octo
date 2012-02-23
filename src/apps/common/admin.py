from django.contrib import admin
from apps.common.models import SpunContent

class SpunContentAdmin(admin.ModelAdmin):
    model = SpunContent
admin.site.register(SpunContent, SpunContentAdmin)
