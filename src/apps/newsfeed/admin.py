from django.contrib import admin
from models import DateFeed,NewsFeed,FeedType

class NewsFeedAdmin(admin.ModelAdmin):
	list_display=('name','location','type','created','expires','active',)


class DateFeedAdmin(admin.ModelAdmin):
	list_display=('date',)


class FeedTypeAdmin(admin.ModelAdmin):
	list_display=('name',)	




admin.site.register(NewsFeed,NewsFeedAdmin)
admin.site.register(DateFeed,DateFeedAdmin)
admin.site.register(FeedType,FeedTypeAdmin)
