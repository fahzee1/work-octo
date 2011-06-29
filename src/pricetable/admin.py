from django.contrib import admin

from pricetable.models import Package

class PackageAdmin(admin.ModelAdmin):
    model = Package
admin.site.register(Package, PackageAdmin)
