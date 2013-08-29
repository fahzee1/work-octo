from django.contrib import admin
from apps.crimedatamodels.models import (CrimesByCity, CityCrimeStats, CrimeContent, 
										 State, CityLocation, ZipCode, MatchAddressLocation,LocalAddress)

class CrimesByCityAdmin(admin.ModelAdmin):
    model = CrimesByCity
    list_filter = ('year','fbi_state',)
admin.site.register(CrimesByCity, CrimesByCityAdmin)

class CityCrimeStatsAdmin(admin.ModelAdmin):
    model = CityCrimeStats
    list_filter = ('year','city__fbi_state',)
admin.site.register(CityCrimeStats, CityCrimeStatsAdmin)

class CrimeContentAdmin(admin.ModelAdmin):
    model = CrimeContent
admin.site.register(CrimeContent, CrimeContentAdmin)
	
class MatchAdressLocationAdmin(admin.ModelAdmin):
	model = MatchAddressLocation
	list_display = ('address','location',)
admin.site.register(MatchAddressLocation,MatchAdressLocationAdmin)

class LocalAddressAdmin(admin.ModelAdmin):
	model = LocalAddress
admin.site.register(LocalAddress,LocalAddressAdmin)

class CityLocationAdmin(admin.ModelAdmin):
	model = CityLocation
	list_filter = ('state',)

admin.site.register(CityLocation,CityLocationAdmin)

class StateAdmin(admin.ModelAdmin):
	model = State
	list_filter = ('name',)

admin.site.register(State,StateAdmin)







