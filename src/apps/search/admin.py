from django.contrib import admin
from apps.search.models import KeywordMatch
from django import forms
from urllib2 import urlopen


class KeywordMatchAdminForm(forms.ModelForm):
    page = forms.ChoiceField(choices=())

    class Meta:
        model = KeywordMatch

    # until the website launches, the choices will be pulled from the
    # sitemap.xml and removing any url that has "search" in it.
    # once we launch, we can use the urls to populate the choices
    def __init__(self, *args, **kwargs):
        super(KeywordMatchAdminForm, self).__init__(*args, **kwargs)
        names = []
        """
        import urls
        for entry in urls.urlpatterns:
            try:
                pname = entry.default_args['extra_context']['page_name']
                names.append((pname,pname))
            except:
                pass
        """
        def getText(nodelist):
            rc = []
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)
            return ''.join(rc)
        
        from xml.dom.minidom import parse, parseString
        import re
        xmlDoc = urlopen('http://www.protectamerica.com/sitemap.xml')
        dom = parseString(xmlDoc.read())
        urls = dom.getElementsByTagName('url')
        for url in urls:
            href = getText(url.getElementsByTagName('loc')[0].childNodes)
            if not re.search(r'search', href):
                names.append((href, href))
        self.fields['page'].choices = names

class KeywordMatchAdmin(admin.ModelAdmin):
    model = KeywordMatch
    form = KeywordMatchAdminForm

admin.site.register(KeywordMatch, KeywordMatchAdmin)
