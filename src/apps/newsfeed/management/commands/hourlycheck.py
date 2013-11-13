from django.core.management.base import BaseCommand, CommandError
from apps.newsfeed.models import TheFeed


class Command(BaseCommand):
	help = 'Check newsfeed objects each hour for expired'

	def handle(self,*args,**options):
		feeds = TheFeed.objects.filter(active=True)
		for x in feeds:
			x.feed_expired()
		self.stdout.write('%s feeds active...' % feeds.count())
