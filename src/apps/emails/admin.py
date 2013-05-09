from django.contrib import admin
from apps.emails.models import Email, EmailImage

class EmailImageInline(admin.TabularInline):
    model = EmailImage

class EmailAdmin(admin.ModelAdmin):
    model = Email
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        EmailImageInline,
    ]
admin.site.register(Email, EmailAdmin)