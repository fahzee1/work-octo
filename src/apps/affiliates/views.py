from apps.affiliates.models import Affiliate, LandingPage, AffTemplate
from apps.common.views import simple_dtt

from django.http import Http404

def affiliate_view(request, affiliate, page_name=None):
    if page_name is None:
        page_name = 'index'
    try:
        affiliate = Affiliate.objects.get(agent_id=affiliate)
    except Affiliate.DoesNotExist:
        raise Http404

    landingpage = LandingPage.objects.get(affiliate=affiliate)
    htmlfilename = 'affiliates/%s/%s' % (landingpage.template.folder, landingpage.get_filename(page_name))

    return simple_dtt(request, htmlfilename, {'page_name': page_name,
        'agent_id': affiliate.agent_id})
