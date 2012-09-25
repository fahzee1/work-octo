from django.contrib import admin
from apps.payitforward.models import Organization, Points

class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
admin.site.register(Organization, OrganizationAdmin)
class PointsAdmin(admin.ModelAdmin):
    model = Points
admin.site.register(Points, PointsAdmin)