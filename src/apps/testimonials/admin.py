from django.contrib import admin
from apps.testimonials.models import Testimonial, Textimonial, Vidimonial,TextimonialCityCache

class TestimonialAdmin(admin.ModelAdmin):
    model = Testimonial
admin.site.register(Testimonial, TestimonialAdmin)
class VidimonialAdmin(admin.ModelAdmin):
    model = Vidimonial
admin.site.register(Vidimonial, VidimonialAdmin)
class TextimonialAdmin(admin.ModelAdmin):
    model = Textimonial
    search_fields = ['message']
    list_filter = ('state',)
admin.site.register(Textimonial, TextimonialAdmin)

class TextimonialCityCacheAdmin(admin.ModelAdmin):
    model = TextimonialCityCache

admin.site.register(TextimonialCityCache, TextimonialCityCacheAdmin)