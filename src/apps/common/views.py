from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.contact.forms import PAContactForm

def simple_dtt(request, template, extra_context):
    
    import urls
 
    def get_active(urllist, name, pages=None):
        if pages is None:
            pages = []
        for entry in urllist:
            try:
                pname = entry.default_args['extra_context']['page_name']
                if pname == name:
                    pages.append(pname)
                    return get_active(urllist, entry.default_args['extra_context']['parent'], pages)
            except:
                pass
        return pages
    pages = get_active(urls.urlpatterns, extra_context['page_name'])
    forms = {}
    forms['basic'] = PAContactForm()
    return render_to_response(template,
                              {'active_pages':pages,
                               'page_name':extra_context['page_name'],
                               'forms': forms},
                              context_instance=RequestContext(request))

