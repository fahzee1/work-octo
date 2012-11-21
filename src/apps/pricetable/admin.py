from django.contrib import admin

from apps.pricetable.models import Package, PackageCode

class PackageAdmin(admin.ModelAdmin):
    model = Package
admin.site.register(Package, PackageAdmin)

class PackageCodeAdmin(admin.ModelAdmin):
    model = PackageCode
admin.site.register(PackageCode, PackageCodeAdmin)