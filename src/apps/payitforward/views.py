from apps.payitforward.models import Organization
from apps.common.views import simple_dtt
from django.utils import simplejson

def point_tracking(request):
    org_data = []
    for org in Organization.objects.all():
        org_data.append((org.points(), '<img src="/media/%s" height="48px" />' % org.image, '%s' % org.color ))

    return simple_dtt(request, 'payitforward/point-tracking.html', {
            'org_data': simplejson.dumps(org_data),
            'page_name': 'payitforward-point-tracking',
            'agent_id': 'i03237',
        })