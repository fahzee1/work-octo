from datetime import datetime, timedelta
from apps.affiliates.models import Affiliate

class AffiliateMiddleware(object):
    
    def process_response(self, request, response):
        expire_time = timedelta(days=90)
        if 'source' in request.GET:
            try:
                affiliate = Affiliate.objects.get(agent_id=request.GET['source'])
                current_cookie = request.COOKIES.get('affiliate', None)
                if not current_cookie:
                    request.session['affiliate'] = affiliate.agent_id
                    response.set_cookie('affiliate', 
                        value=affiliate.agent_id,
                        expires=datetime.now() + expire_time)
            except Affiliate.DoesNotExist:
                pass
        return response
