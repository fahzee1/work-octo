from django.contrib import admin
from apps.crimedatamodels.models import CrimesByCity, CityCrimeStats, CrimeContent

class CrimesByCityAdmin(admin.ModelAdmin):
    model = CrimesByCity
admin.site.register(CrimesByCity, CrimesByCityAdmin)

class CityCrimeStatsAdmin(admin.ModelAdmin):
    model = CrimesByCity
admin.site.register(CityCrimeStats, CityCrimeStatsAdmin)

class CrimeContentAdmin(admin.ModelAdmin):
    model = CrimeContent
admin.site.register(CrimeContent, CrimeContentAdmin)
