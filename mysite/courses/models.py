from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from mysite.blog.models import Blog
from mysite.shared import bibutils
import datetime
import re

class Department(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField()
    def __unicode__(self):
        return self.name

class Instructor(models.Model):
    name = models.CharField(max_length=9)
    url = models.URLField()
    def __unicode__(self):
        return self.name

class Course(models.Model):
    YEAR_CHOICES = (
        (2011, '2011'),
        (2012, '2012'),
        (2013, '2013'),
        (2014, '2014'),
        (2015, '2015'),
        (2016, '2016'),
    )        
    SEMESTER_CHOICES = (
        ('sp', 'Spring'),
        ('fa', 'Fall'),
    )
    department = models.ForeignKey('Department', related_name='courses')
    instructor = models.ForeignKey('Instructor', related_name='courses')
    students = models.ManyToManyField(User, related_name='courses')
    number = models.CharField(max_length=20)
    slug = models.CharField(max_length=20)
    title = models.CharField(max_length=80)
    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    times = models.CharField(max_length=64)
    location = models.CharField(max_length=32)
    ereserves_id = models.CharField(max_length=8, blank=True)
    description = models.TextField()
    blurb = models.TextField(blank=True)
    evaluation = models.TextField(blank=True)
    participation = models.TextField(blank=True)
    thanks = models.TextField(blank=True)
    is_archived = models.BooleanField(default=False)
    has_blog = models.BooleanField(default=False)
    def has_student(self, student):
        return (len(self.students.filter(id=student.id, is_active=True)) > 0)
    def is_authorized(self, user):
        return user.is_staff or self.has_student(user)
    def get_date_range(self):
        if self.semester == 'sp':
            start_day = 1
            start_month = 1
            end_day = 30
            end_month = 4
        elif self.semester == 'fa':
            start_day = 1
            start_month = 8
            end_day = 31
            end_month = 12
        else: # summer
            start_day = 1
            start_month = 5
            end_day = 31
            end_month = 7
        return (datetime.date(self.year, start_month, start_day),
                datetime.date(self.year, end_month, end_day))
    @models.permalink
    def get_absolute_url(self):
        return ('course_info_view', (), { 
                'slug': self.slug, 
                'semester': self.semester, 
                'year': self.year }) 
    def __unicode__(self):
        return u'%s: %s, %s %s' % (
            self.number, self.title,
            self.get_semester_display(), self.get_year_display())
    class Meta:
        unique_together = ('slug', 'semester', 'year')
        ordering = ('-year', 'semester')

class Meeting(models.Model):
    course = models.ForeignKey('Course', related_name='meetings')
    date = models.DateField()
    title = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    readings = models.ManyToManyField('Reading', through='ReadingAssignment', blank=True)
    is_tentative = models.BooleanField(default=True)
    def upload_to(o, filename):
        return 'courses/%s/%s/%s/slides/%s.pdf' % (
            o.course.slug, 
            o.course.year, 
            o.course.semester, 
            o.date.strftime('%m-%d'))
    slides = models.FileField(upload_to=upload_to, blank=True, null=True)
    def has_readings(self):
        return len(self.readings.all()) > 0
    def has_ereserves(self):
        for reading in self.readings.all():
            if reading.access_via_ereserves:
                return True
        return False
    def reading_list(self):
        return self.readings.all().order_by('readingassignment__order')
    def __unicode__(self):
        return u'%s: %s' % (self.date.strftime('%m-%d'), self.title)
    class Meta:
        ordering = ('course','date')

class Holiday(models.Model):
    course = models.ForeignKey('Course', related_name='holidays')
    date = models.DateField()
    name = models.CharField(max_length=80)
    def is_holiday(self):
        return True # For mixing holidays and meetings in schedule lists
    def __unicode__(self):
        return u'%s: %s' % (self.date.strftime('%m-%d'), self.name)
    class Meta:
        ordering = ('date',)

class Assignment(models.Model):
    course = models.ForeignKey('Course', related_name='assignments')
    slug = models.SlugField()
    due_date = models.DateField(blank=True)
    title = models.CharField(max_length=80)
    description = models.TextField()
    points = models.IntegerField(default=0)
    is_handed_out = models.BooleanField(default=False)
    is_submitted_online = models.BooleanField(default=False)
    is_graded = models.BooleanField(default=False)
    def get_absolute_url(self):
        return (reverse('course_assignments_view', kwargs={ 
                    'slug': self.course.slug, 
                    'semester': self.course.semester, 
                    'year': self.course.year }) + '#' + self.slug)
    def get_submit_url(self):
        return (reverse('course_submit_assignment_view', kwargs={
                    'assignment_id': self.id }))
    def __unicode__(self):
        if self.due_date:
            return u'%s %s: %s' % (
                self.course.number, self.due_date.strftime('%m-%d'), self.title)
        else:
            return u'%s: %s' % (self.course.number, self.title)
    class Meta:
        ordering = ('due_date',)

class Submission(models.Model):
    assignment = models.ForeignKey('Assignment', related_name='submissions')
    submitter = models.ForeignKey(User, related_name='submissions')
    def upload_to(o, filename):
        return 'courses/%s/%s/%s/assignments/%s/%s.zip' % (
            o.assignment.course.slug, 
            o.assignment.course.year, 
            o.assignment.course.semester, 
            o.assignment.slug,
            o.submitter.username)
    zipfile = models.FileField(upload_to=upload_to)
    grade = models.IntegerField(default=0)
    comments = models.TextField(blank=True)
    def __unicode__(self):
        return u'%s: %s' % (self.assignment, self.submitter.get_full_name())

PROXY = 'http://libproxy.lib.unc.edu/login?url='

class Linky:
    def __init__(self, stored_url, access_via_proxy, ignore_citation_url):
        self.url = ''
        self.stored_url = stored_url
        self.access_via_proxy = access_via_proxy
        self.ignore_citation_url = ignore_citation_url
    def linkify(self, html):
        html = re.sub(r' (https?://.+)\.', self.repl, html, 1)
        if self.stored_url and not self.url == self.stored_url:
            if self.access_via_proxy:
                anchor = self.stored_url[len(PROXY):]
            elif self.stored_url.startswith('/'):
                anchor = 'PDF'
            else:
                anchor = self.stored_url
            html = re.sub(
                r'</div>\n</div>', 
                r' <a href="%s">%s</a>.</div>\n</div>' % (
                    self.stored_url, anchor), html, 1)
        return mark_safe(html)
    def repl(self, match):
        if self.ignore_citation_url:
            return ''
        self.url = match.group(1)
        if self.access_via_proxy:
            self.url = PROXY + self.url
        return ' <a href="%s">%s</a>.' % (self.url, match.group(1))

class Reading(models.Model):
    zotero_id = models.CharField(max_length=16)
    citation_text = models.CharField(max_length=128, blank=True, editable=False)
    citation_html = models.TextField(blank=True, editable=False)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='courses/readings', blank=True)
    url = models.URLField(blank=True, verify_exists=False)
    access_via_proxy = models.BooleanField(default=False)
    access_via_ereserves = models.BooleanField(default=False)
    ignore_citation_url = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if self.zotero_id:
            self.citation_text = bibutils.format_zotero_as_text(self.zotero_id)
            self.citation_html = bibutils.format_zotero_as_html(self.zotero_id)
        super(Reading, self).save(*args, **kwargs)
    def get_url(self):
        if self.file:
            return self.file.url
        if self.url:
            if self.access_via_proxy:
                return PROXY + self.url
            else:
                return self.url
        return ''
    def as_html(self):
        linky = Linky(
            self.get_url(), self.access_via_proxy, self.ignore_citation_url)
        return linky.linkify(self.citation_html)
    def __unicode__(self):
        return self.citation_text
    class Meta:
        ordering = ('citation_text',)

class ReadingAssignment(models.Model):
    meeting = models.ForeignKey('Meeting', related_name='reading_assignments')
    reading = models.ForeignKey('Reading')
    order = models.IntegerField(blank=True, null=True)
    discussion_leader = models.ForeignKey(User, blank=True, null=True)
    discussion_questions = models.TextField(blank=True)
    def discussion_questions_posted(self):
        return len(self.discussion_questions.strip()) > 0
    @models.permalink
    def get_absolute_url(self):
        return ('course_discussion_view', (), { 
                'discussion_id': self.id }) 
    class Meta:
        ordering = ('order',)
