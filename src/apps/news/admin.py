from django.contrib import admin
from apps.news.models import Category, Article

class CategoryAdmin(admin.ModelAdmin):
    model = Category
admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    search_fields = ['heading','content','summary']
admin.site.register(Article, ArticleAdmin)

