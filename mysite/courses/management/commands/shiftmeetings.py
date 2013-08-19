from django.core.management.base import CommandError
from django.db import transaction
from utils import MyBaseCommand

class Command(MyBaseCommand):
    help = 'Shifts the dates of course meetings.'
    @transaction.commit_on_success
    def handle(self, *args, **options):
        course = self.input_course()
        for m in course.meetings.all():
            self.stdout.write('%s\n' % m)
        start_date = self.input_date('Start date')
        end_date = self.input_date('End date')
        self.stdout.write('Shift in which direction ?\n')
        direction = self.input_choices(['forward','backward'])
        if direction == 'forward':
            meetings = list(course.meetings.filter(
                    date__gte=start_date, date__lte=end_date))
        else:
            meetings = list(reversed(course.meetings.filter(
                    date__gte=start_date, date__lt=end_date)))
        for i, m in list(enumerate(meetings))[1:-1]:
            if not m.is_tentative:
                raise CommandError('%s has been finalized.' % m)
            new_date =  meetings[i+1].date
            self.stdout.write('%s -> %s\n' % (m, new_date))
            m.date = new_date
        if self.input_ok('Shifting %s meetings' % len(meetings)):
            for m in meetings:
                m.save()
            self.stdout.write('Shifted %s meetings.\n' % len(meetings))
