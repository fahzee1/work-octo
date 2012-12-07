import datetime

from django.db.models import Q

from models import Ad, Campaign, AdSpot

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
    ad_dict = dict((str(spot.slug), None) for spot in AdSpot.objects.all())
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
                    if ctx['pa_ads'][ad.type.slug] is None:
                        ctx['pa_ads'][ad.type.slug] = ad
        except Ad.DoesNotExist:
            pass
    return ctx