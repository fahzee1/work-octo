import csv
import os
import datetime
import calendar

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.contact.models import CEOFeedback

class Command(BaseCommand):
    help = 'Generates a month to date textimonial report'

    def handle(self, *args, **options):

        today = datetime.datetime.today()
        monthrange = calendar.monthrange(today.year, today.month)
        first_day = datetime.datetime(today.year, today.month, 1, 0, 0, 0)
        last_day = datetime.datetime(today.year, today.month, monthrange[1], 23, 59, 59)
        feedbacks = CEOFeedback.objects.filter(date_created__lte=last_day, date_created__gte=first_day)

        if not feedbacks:
            print 'no feedbacks'
            return None
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'month_to_date_ceo_feedbacks.csv')
        writer = csv.writer(open(csv_file_path, 'w'),
            delimiter=',', quotechar='"')

        writer.writerow([
            'name',
            'email',
            'phone',
            'city',
            'state',
            'feedback_type',
            'department',
            'rep_name',
            'message',
            'rating',
            'date_created',
            'ip_address',
        ])
        for feedback in feedbacks:
            writer.writerow([
                feedback.name.encode('ascii', 'ignore'),
                feedback.email.encode('ascii', 'ignore'),
                feedback.phone.encode('ascii', 'ignore'),
                feedback.city,
                feedback.state,
                feedback.feedback_type,
                feedback.department,
                feedback.rep_name,
                feedback.message.encode('ascii', 'ignore'),
                feedback.rating,
                feedback.date_created,
                feedback.ip_address,
            ])