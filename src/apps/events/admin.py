from django.contrib import admin
from apps.events.models import Event, Venue


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue')
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state')

admin.site.register(Event, EventAdmin)

admin.site.register(Venue, VenueAdmin)