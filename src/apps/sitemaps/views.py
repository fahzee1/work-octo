import urls

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

def index(request):
    
    def sort_urls(urllist, parent=None):
        count = 0
        pages = ''
        for entry in urllist:
            # get pages that have context only
            try:
                context = entry.default_args['extra_context']
                if context['parent'] == parent:
                    page_name = context['page_name'].replace('-', ' ').capitalize()
                    pages = pages + '<li'
                    if parent:
                        pages = pages + ' class="child"'
                    pages = pages + '> %s ' % (page_name)
                    cpages = sort_urls(urllist, parent=context['page_name'])
                    pages = pages + cpages
                    pages = pages + '</li>'

                    count = count + 1
            except:
                pass
        if count > 0:
            return '<ul>' + pages + '</ul>'
        return pages
    pages = sort_urls(urls.urlpatterns)
    return render_to_response('sitemaps/sitemap.html', {'pages':pages},
                              context_instance=RequestContext(request))
