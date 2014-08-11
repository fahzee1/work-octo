from django.contrib import admin
from apps.crimedatamodels.models import (CrimesByCity, CityCrimeStats, CrimeContent,
										 State, CityLocation, ZipCode, MatchAddressLocation,LocalAddress,StateCrimeStats,
										 FeaturedIcon,FeaturedVideo,CityCompetitor, Resources,Permits)

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

class CrimeStateAdmin(admin.ModelAdmin):
	model = StateCrimeStats

admin.site.register(StateCrimeStats,CrimeStateAdmin)


class FeaturedIconAdmin(admin.ModelAdmin):
	model = FeaturedIcon
	raw_id_fields = ('city',)
	readonly_fields = ('image_height','image_width')

admin.site.register(FeaturedIcon,FeaturedIconAdmin)

class FeaturedVideoAdmin(admin.ModelAdmin):
	model = FeaturedVideo
	raw_id_fields = ('city',)

admin.site.register(FeaturedVideo,FeaturedVideoAdmin)

class CityCompeteAdmin(admin.ModelAdmin):
	model = CityCompetitor
	raw_id_fields = ('city',)

admin.site.register(CityCompetitor,CityCompeteAdmin)



class ResourcesAdmin(admin.ModelAdmin):
    model = Resources
    raw_id_fields = ('city',)

admin.site.register(Resources,ResourcesAdmin)

admin.site.register(Permits)


