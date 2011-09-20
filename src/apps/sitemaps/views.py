import urls

from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    
    def sort_urls(urllist, parent=None):
        count = 0
        pages = ''
        for entry in urllist:
            # get pages that have context only
            try:
                context = entry.default_args['extra_context']
                if context['parent'] == parent:
                    pages = pages + '<li> %s ' % (context['page_name'])
                    cpages = sort_urls(urllist, parent=context['page_name'])
                    pages = pages + cpages
                    pages = pages + '</li>'

                    count = count + 1
            except:
                pass
        if count > 0:
            return '<ul>' + pages + '</ul>'
        return pages
    def list_urls(urllist, parent=None):
        count = 0
        pages = []
        for entry in urllist:
            try:
                context = entry.default_args['extra_context']
                if context['parent'] == parent:
                    dic = {'name': context['page_name']}
                    cpages = list_urls(urllist, parent=context['page_name'])
                    if len(cpages):
                        dic['children'] = cpages
                    pages.append(dic)
            except:
                pass
        return pages
                
    pages = sort_urls(urls.urlpatterns)

    list_pages = list_urls(urls.urlpatterns)
    print list_pages
    div1 = '<div>'
    div2 = '<div>'
    div3 = '<div>'
    div4 = '<div>'
    div_list = [div1, div2, div3, div4]
    count = 0
    for pagel in list_pages:
        
        div_list[count] = div_list[count] + pagel['name']

        count = count + 1
        if count == 4:
            count = 0
    print div_list
    return render_to_response('sitemaps/sitemap.html', {'pages':pages},
                              context_instance=RequestContext(request))
