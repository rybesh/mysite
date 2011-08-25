from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from mysite.courses.models import Course
from django.db import transaction
import csv

class Command(BaseCommand):
    args = '<csv_filename>'
    help = 'Creates student accounts and adds them to a course.'
    @transaction.commit_on_success
    def handle(self, *args, **options):
        if not len(args) == 1:
            raise CommandError(
                'You must provide the name of (just) one CSV file with student info.')
        students = []
        new_count = existing_count = 0
        for row in csv.DictReader(open(args[0], 'rb')):
            try:
                last_name, first_name = row['Name'].split(',')
                email = row['Email']
                username = first_name[0].lower() + last_name.lower()
                student, created = User.objects.get_or_create(
                    first_name=first_name, last_name=last_name,
                    defaults={ 'username': username })
                if created:
                    new_count += 1
                else:
                    existing_count += 1
                student.email = email
                student.save()
                students.append(student)
            except KeyError as e:
                raise CommandError('%s is missing a %s value.' % (args[0], e))
        self.stdout.write('%s new students and %s existing students.\n' % (new_count, existing_count))
        self.stdout.write('To which course will these students be added?\n')
        for course in Course.objects.filter(is_archived=False):
            self.stdout.write('(%s) %s\n' % (course.id, course))
        while True:
            course_id = raw_input('Course ID: ')
            try:
                course = Course.objects.get(id=course_id)
                break
            except (ValueError, Course.DoesNotExist):
                self.stdout.write('Please choose one of the course IDs listed above.\n')
        added_count = existing_count = 0
        for student in students:
            if course.has_student(student):
                existing_count += 1
            else:
                course.students.add(student)
                added_count += 1
        self.stdout.write('%s students added (%s already in that course).\n' % (added_count, existing_count))
        
        
            
            
            
            
            
        
        
