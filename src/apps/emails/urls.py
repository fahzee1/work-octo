from django.conf.urls.defaults import *

urlpatterns = patterns('apps.emails.views',
    # email url
    url(r'^(?P<email_slug>[a-zA-Z0-9\-]+)_(?P<email_id>\d+)/$', 'render_email', name="render_email"),
)