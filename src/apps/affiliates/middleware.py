from datetime import datetime, timedelta

from django.conf import settings

from apps.affiliates.models import Affiliate


class AffiliateMiddleware(object):
    
    def process_response(self, request, response):

        expire_time = timedelta(days=90)

        # get default agent id from settings

        try:
            default_agent = settings.DEFAULT_AGENTID
        except AttributeError:
            default_agent = None

        current_cookie = request.COOKIES.get('refer_id', None)
        if not current_cookie:
            if 'agent' in request.GET:
                try:
                    affiliate = Affiliate.objects.get(agent_id=request.GET['agent'])
                    request.session['refer_id'] = affiliate.agent_id
                    response.set_cookie('refer_id',
                        value=affiliate.agent_id,
                        expires=datetime.now() + expire_time)
                except Affiliate.DoesNotExist:
                    pass
            else:
                if default_agent is not None:
                    request.session['refer_id'] = default_agent
                    response.set_cookie('refer_id',
                        value=default_agent,
                        expires=datetime.now() + expire_time)

        if 'affkey' in request.GET:
            request.session['affkey'] = request.GET['affkey']
            # Allow overwriting of affkey cookie
            response.set_cookie('affkey',
                value=request.GET['affkey'],
                expires=datetime.now() + expire_time)
        if 'source' in request.GET:
            request.session['source'] = request.GET['source']
            # Allow overwriting of affkey cookie
            response.set_cookie('source',
                value=request.GET['source'],
                expires=datetime.now() + expire_time)
        return response
