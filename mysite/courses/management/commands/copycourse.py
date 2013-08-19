from datetime import timedelta
from django.core.management.base import CommandError
from django.db import transaction
from mysite.courses.models import Meeting, ReadingAssignment
from utils import MyBaseCommand

def push_from_weekend(date, days):
    if date.weekday() > 3: # Friday or weekend
        if days == 'MW': 
            nextday = 7
        else:    # TTH
            nextday = 8 
        return date + timedelta(days=(nextday-date.weekday()))
    return date
        
class Command(MyBaseCommand):
    help = 'Copies all meetings from an old course to a new course.'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        self.stdout.write('Choose the old course:\n')
        old_course = self.input_course(include_archived=True)
        old_meetings = old_course.meetings.all()
        self.stdout.write('Choose the new course:\n')
        new_course = self.input_course()
        start_date = self.input_date('Start date of new course')
        delta = start_date - old_meetings[0].date
        self.stdout.write('What days does the new course meet?\n')
        days = self.input_choices(['MW','TTH'])
        pre_m = None
        for old_m in old_meetings:
            new_m = Meeting()
            new_m.course = new_course
            new_m.date = push_from_weekend(old_m.date + delta, days)
            if pre_m and new_m.date == pre_m.date:
                new_m.date = push_from_weekend(
                    new_m.date + timedelta(days=2), days)
            new_m.title = old_m.title
            new_m.description = old_m.description
            new_m.save()
            for ra in ReadingAssignment.objects.filter(meeting=old_m):
                ra.pk = None # create a new ReadingAssignment with same props
                ra.meeting = new_m
                ra.save()
            self.stdout.write('%s\n' % new_m)
            pre_m = new_m
        if not self.input_ok('Keep these changes'):
            raise CommandError('Course was not copied.')
