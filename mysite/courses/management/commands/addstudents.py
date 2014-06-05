from django.contrib.auth.models import User
from django.core.management.base import CommandError
from django.db import transaction
from django.db.utils import IntegrityError
from mysite.courses.models import Course
from utils import MyBaseCommand
from HTMLParser import HTMLParser
import csv

def parse_csv(filename):
    for row in csv.DictReader(open(filename, 'rb')):
        last_name, first_name = row['Name'].split(',')
        email = row['Email']
        yield (lastname, first_name, email)

class TableReader(HTMLParser):
    def read(self, f):
        self.tag = None
        self.data = ''
        self.keys = []
        self.rows = []
        self.keyindex = 0
        for line in f:
            self.feed(line.strip())
        return self.rows
    def handle_starttag(self, tag, attrs):
        self.tag = tag
        if tag == 'tr':
            if len(self.keys) > 0:
                self.rows.append({})
                self.keyindex = 0
    def handle_endtag(self, tag):
        if self.tag == 'th':
            self.keys.append(self.data)
        elif self.tag == 'td':
            key = self.keys[self.keyindex]
            self.rows[-1][key] = self.data
            self.keyindex += 1
        self.tag = None
        self.data = ''
    def handle_data(self, data):
        self.data += data

class Command(MyBaseCommand):
    args = '<student_info_file> <emails_file>'
    help = 'Creates student accounts and adds them to a course.'
    @transaction.commit_on_success
    def handle(self, *args, **options):
        if not len(args) == 2:
            raise CommandError(
                'You must provide the names of files with student info and emails.')
        if args[0].endswith('.csv'):
            reader = csv.DictReader
        elif args[0].endswith('.xls'):
            reader = TableReader().read
        else:
            raise CommandError(
                'Student info must be in CSV or XLS (really HTML).')
        emails = []
        with open(args[1]) as f:
            for line in f:
                emails.append(line.strip())
        students = []
        new_count = existing_count = 0
        for i, row in enumerate(reader(open(args[0], 'rb'))):
            try:
                last_name, first_name = [ 
                    x.strip() for x in row['Name'].split(',') ]
                email = emails[i]
                username = email.split('@')[0]
                try:
                    student, created = User.objects.get_or_create(
                        first_name=first_name, last_name=last_name,
                        defaults={ 'username': username })
                    if created:
                        self.stdout.write(
                            'New student: %s %s (%s)\n' 
                            % (first_name, last_name, email))
                        new_count += 1
                    else:
                        self.stdout.write(
                            'Old student: %s %s (%s)\n' 
                            % (first_name, last_name, email))
                        existing_count += 1
                    student.email = email
                    student.is_active = True
                    student.save()
                    students.append(student)
                except IntegrityError as e:
                    raise CommandError('Username collision: %s' % username)
            except KeyError as e:
                raise CommandError('%s is missing a %s value.' % (args[0], e))
        if not len(students) == len(emails):
            raise CommandError(
                'Number of emails does not match number of students.')
        self.stdout.write('%s new students and %s existing students.\n' % (new_count, existing_count))
        self.stdout.write('To which course will these students be added?\n')
        course = self.input_course()
        added_count = existing_count = 0
        for student in course.students.all():
            if not student in students:
                self.stdout.write('%s appears to have dropped the course.\n' % student.email)
        for student in students:
            if course.has_student(student):
                existing_count += 1
            else:
                course.students.add(student)
                self.stdout.write('%s\n' % student.email)
                added_count += 1
        self.stdout.write('%s students added (%s already in that course).\n' % (added_count, existing_count))
        
        
            
            
            
            
            
        
        
