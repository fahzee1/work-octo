from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^protectamerica/', include('protectamerica.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls'))

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    #contact us
    url(r'^contact/ajaxpost/?$', 'apps.contact.views.ajax_post'),
    url(r'^contact-us/?$', 'apps.contact.views.main', name='contact-us'),
    url(r'^contact-us/feedback-to-the-ceo/?$', 'apps.contact.views.ceo',
        name='feedback-ceo'),
    url(r'^contact-us/find-us/?$', 'apps.contact.views.find_us', name='find-us'),
    url(r'^products/order-package/?$', 'apps.contact.views.order_form',
        name='order-package'),
    url(r'^sitemap/$', 'apps.sitemaps.views.index', name='sitemap'),

    # affiliate urls
    url(r'^affiliate/(?P<affiliate>[a-zA-Z0-9]+)/$', 'apps.affiliates.views.affiliate_view', name='affiliate'),
    url(r'^affiliate/(?P<affiliate>[a-zA-Z0-9]+)/(?P<page_name>.*)/$', 'apps.affiliates.views.affiliate_view', name='affiliate_inside'),

    # search urls
    url(r'^search/$', 'apps.search.views.search', name='search'),
)

# a simple direct_to_template wrapper
def dtt(pattern, template, name, parent=None, ctx=None):
    ctx = ctx or {}


    context = dict(page_name=name, parent=parent)
    context.update(ctx)

    return url(pattern, 'apps.common.views.simple_dtt',
		dict(template=template, extra_context=context),
		name=name)

urlpatterns += patterns('',

    # Home Page
    dtt(r'^$', '_base.html', 'home', ctx={'page_name': 'index'}),
    dtt(r'^thank-you/$', 'thank-you.html', 'thankyou', ctx={'page_name': 'thankyou'}),
    dtt(r'^cswitch/$', 'content_switch.html', 'cswitch', ctx={'page_name': 'index'}),

)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
