from django.shortcuts import render_to_response
from django.template import RequestContext

from urllib import unquote

from apps.search.models import KeywordMatch

def search(request):
    pages = []
    height = 0
    if 'q' in request.GET:
        q = unquote(request.GET['q'])
        pageObj = KeywordMatch.objects.filter(keyword=q)
        for page in pageObj:
            details = page.get_page_details()
            if details is not None:
                pages.append({'title': details['title'],'description': details['description'],'url': details['url']})
        height = 0
        if pageObj:
            height = ((len(pages) * 120) + 50)

    return render_to_response('search.html', {'pages': pages, 'height': height}, context_instance=RequestContext(request))
