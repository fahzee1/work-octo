from django.contrib import admin
from apps.common.models import SpunContent,BlackFriday

class SpunContentAdmin(admin.ModelAdmin):
    model = SpunContent
admin.site.register(SpunContent, SpunContentAdmin)

class BlackFridayAdmin(admin.ModelAdmin):
    model = BlackFriday
admin.site.register(BlackFriday, BlackFridayAdmin)
