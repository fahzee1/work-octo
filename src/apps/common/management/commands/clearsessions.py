from django.core.management.base import BaseCommand, CommandError
from django.contrib.sessions.models import Session
from datetime import datetime
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Clears all expired sessions'

    def handle(self, *args, **options):
    	sessions = Session.objects.filter(expire_date__lt=datetime.now())
    	ct = sessions.count()
    	sessions.delete()
    	send_mail('Deleted %s sessions' % ct, 'Test email to let you know I deleted %s sessions last night' % ct,
    		       'noreply@protectamerica.com',['cjogbuehi@protectamerica.com'])
    	self.stdout.write('Deleted %s sessions' % ct)
