from django.core.management.base import BaseCommand, CommandError
import urls
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.conf import settings
from django.template import RequestContext

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        def show_urls(urllist, url_list, depth=0):
            for entry in urllist:
                #print "  " * depth, entry.regex.pattern
                if hasattr(entry, 'name'):
                    if entry.name:
                        url_list.append({
                            'name': entry.name, 
                            'url':reverse(entry.name),
                        })
            return url_list
        
        #url_l = []
        #for url in show_urls(urls.urlpatterns, []): 
        url_l = show_urls(urls.urlpatterns, [])
        t = loader.get_template('sitemaps/sitemap.html')
        c = Context({
            'urls': url_l,
            'MEDIA_URL': settings.MEDIA_URL
        })
        #print '%s/sitemaps/static/sitemap.html' % settings.TEMPLATE_DIRS[0]
        f = open('%s/sitemaps/static/sitemap.html' % 
            settings.TEMPLATE_DIRS[0], 'w' )
        f.write(t.render(c))
        f.close()
