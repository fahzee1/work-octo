import datetime

from django.db.models import Q

from models import Ad, Campaign, TYPE_CHOICES

WEEKDAYS = (
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',
)   

def campaign(request):
    ad_dict = dict((key, None) for (key, value) in TYPE_CHOICES)
    ctx = {'pa_campaign': [], 'pa_ads': ad_dict}
    today = datetime.date.today()
    weekday = datetime.date.today().weekday()
    campaigns = Campaign.objects.filter(
            Q(start_date__lte=today) | Q(start_date__isnull=True)
        ).filter(
            Q(end_date__gte=today) | Q(end_date__isnull=True)
        ).order_by('-pk')
    for campaign in campaigns:
        try:
            if campaign.__getattribute__(WEEKDAYS[weekday]):
                ctx['pa_campaign'].append(campaign)
                for ad in campaign.ad_set.all():
                    if ctx['pa_ads'][ad.type] is None:
                        ctx['pa_ads'][ad.type] = ad
        except Ad.DoesNotExist:
            pass
    return ctx