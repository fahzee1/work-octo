from django.contrib import admin
from apps.crimedatamodels.models import (CrimesByCity, CityCrimeStats, CrimeContent, 
										 State, CityLocation, ZipCode, MatchAddressLocation,LocalAddress)

class CrimesByCityAdmin(admin.ModelAdmin):
    model = CrimesByCity
admin.site.register(CrimesByCity, CrimesByCityAdmin)

class CityCrimeStatsAdmin(admin.ModelAdmin):
    model = CrimesByCity
admin.site.register(CityCrimeStats, CityCrimeStatsAdmin)

class CrimeContentAdmin(admin.ModelAdmin):
    model = CrimeContent
admin.site.register(CrimeContent, CrimeContentAdmin)
	
class MatchAdressLocationAdmin(admin.ModelAdmin):
	model=MatchAddressLocation
	list_display=('address','location',)
admin.site.register(MatchAddressLocation,MatchAdressLocationAdmin)

class LocalAddressAdmin(admin.ModelAdmin):
	model=LocalAddress
admin.site.register(LocalAddress,LocalAddressAdmin)

class CityLocationAdmin(admin.ModelAdmin):
	model=CityLocation
admin.site.register(CityLocation,CityLocationAdmin)




