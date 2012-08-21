import os

from django.http import Http404, HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.cache import never_cache
from django.conf import settings

from apps.emails.models import Email, EmailImage

@never_cache
def render_email(request, email_slug, email_id):
    try:
        email = Email.objects.get(id=email_id)
    except Email.DoesNotExist:
        raise Http404

    EMAIL_IMAGE_URL = os.path.join(settings.MEDIA_URL, 'email_images', 'email_%s' % email.id) + '/'
    t = loader.get_template_from_string(email.html)
    c = RequestContext(request)
    c['EMAIL_IMAGE_URL'] = EMAIL_IMAGE_URL

    return HttpResponse(t.render(c))