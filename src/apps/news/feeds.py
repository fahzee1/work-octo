from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from apps.news.models import Article

class RssNewsFeedGenerator(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(RssNewsFeedGenerator, self).add_item_elements(handler, item)
        if 'image' in item:
            handler.addQuickElement(u'enclosure', '', {
                'url': item['image'],
                'type': 'image/jpeg',
                'size': item['image_size'],
            })

class RssNewsFeed(Feed):
    feed_type = RssNewsFeedGenerator
    title = 'Protect America\'s News Feed'
    link = '/news/'
    description = 'The latest news in the Home Security industry'

    def item_extra_kwargs(self, obj):
        """
        Returns an extra keyword arguments dictionary that is used with
        the `add_item` call of the feed generator.
        Add the 'content' field of the 'Entry' item, to be used by the custom feed generator.
        """
        image_url = None
        image_size = None
        if obj.image:
            image_url = obj.image.url
            image_size = obj.image.size
        return {
            'image': 'http://www.protectamerica.com%s' % image_url,
            'image_size': str(image_size),
            }    

    def items(self):
        return Article.objects.order_by('-date_created')[:10]

