from django.core.management.base import CommandError
from django.db import transaction
from utils import MyBaseCommand

class Command(MyBaseCommand):
    help = 'Shifts forward the dates of course meetings.'
    @transaction.commit_on_success
    def handle(self, *args, **options):
        course = self.input_course()
        for m in course.meetings.all():
            self.stdout.write('%s\n' % m)
        start_date = self.input_date('Start date')
        end_date = self.input_date('End date')
        meetings = list(course.meetings.filter(
            date__gte=start_date, date__lt=end_date))
        for i, m in enumerate(meetings):
            if not m.is_tentative:
                raise CommandError('%s has been finalized.' % m)
            if (i+1) == len(meetings):
                m.date = end_date
            else:
                m.date = meetings[i+1].date
        if self.input_ok('Shifting %s meetings' % len(meetings)):
            for m in meetings:
                m.save()
                self.stdout.write('%s\n' % m)
            self.stdout.write('Shifted %s meetings.\n' % len(meetings))
