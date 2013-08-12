from django.contrib import admin
from models import TheFeed,AddType,FallBacks,TweetBackup

class NewsFeedAdmin(admin.ModelAdmin):
	list_display=('name','location','type','created','expires','active','feed_expired',)
	list_filter=('type','active','state',)
	search_fields=('name','created',)


class FeedTypeAdmin(admin.ModelAdmin):
	list_display=('name',)	

class FallBackAdmin(admin.ModelAdmin):
	list_display=('feed_name',)	

class TweetsAdmin(admin.ModelAdmin):
	list_display=('text','GetRelativeCreatedAt','created',)


admin.site.register(TweetBackup,TweetsAdmin)
admin.site.register(TheFeed,NewsFeedAdmin)
admin.site.register(AddType,FeedTypeAdmin)
admin.site.register(FallBacks,FallBackAdmin)
