from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import bibutils

class Department(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField()
    def __unicode__(self):
        return self.name

class Instructor(models.Model):
    name = models.CharField(max_length=9)
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    office = models.CharField(max_length=12)
    office_hours = models.CharField(max_length=32)
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
        ('su', 'Summer'),
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
    times = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    description = models.TextField()
    def has_student(self, student):
        return (len(self.students.filter(id=student.id, is_active=True)) > 0)
    def is_authorized(self, user):
        return user.is_staff or self.has_student(user)
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

class Meeting(models.Model):
    course = models.ForeignKey('Course', related_name='meetings')
    date = models.DateField()
    title = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    topics = models.ManyToManyField('Topic', blank=True)
    readings = models.ManyToManyField('Reading', through='ReadingAssignment', blank=True)
    is_tentative = models.BooleanField(default=True)
    def has_readings(self):
        return len(self.readings.all()) > 0
    def reading_list(self):
        return self.readings.all().order_by('readingassignment__order')
    def get_topic_names(self):
        return self.topics.values_list('name', flat=True)
    def __unicode__(self):
        return u'%s: %s' % (self.date.strftime('%m-%d'), self.title)
    class Meta:
        ordering = ('date',)

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

class Topic(models.Model):
    name = models.CharField(max_length=80)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ('name',)

class Assignment(models.Model):
    course = models.ForeignKey('Course', related_name='assignments')
    slug = models.SlugField()
    due_date = models.DateField()
    title = models.CharField(max_length=80)
    description = models.TextField()
    is_handed_out = models.BooleanField(default=False)
    def get_absolute_url(self):
        return (reverse('course_assignments_view', kwargs={ 
                'slug': self.course.slug, 
                'semester': self.course.semester, 
                'year': self.course.year }) + '#' + self.slug)
    def __unicode__(self):
        return u'%s: %s' % (self.due_date.strftime('%m-%d'), self.title)
    class Meta:
        ordering = ('due_date',)

class Reading(models.Model):
    bibtex = models.TextField()
    citekey = models.CharField(max_length=16, editable=False, unique=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='courses/readings', blank=True)
    url = models.URLField(blank=True, verify_exists=False)
    def save(self, *args, **kwargs):
        citekeys = bibutils.citekeys(self.bibtex)
        if not len(citekeys) == 1:
            raise Exception('Must have exactly 1 citekey, got %s' % citekeys)
        self.citekey = citekeys[0]
        super(Reading, self).save(*args, **kwargs)
    def as_html(self):
        return bibutils.format_as_html(self.bibtex)
    def __unicode__(self):
        return bibutils.format_as_text(self.bibtex)
    class Meta:
        ordering = ('citekey',)

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
