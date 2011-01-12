# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Department'
        db.create_table('courses_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('courses', ['Department'])

        # Adding model 'Course'
        db.create_table('courses_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courses', to=orm['courses.Department'])),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('semester', self.gf('django.db.models.fields.IntegerField')()),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('times', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('courses', ['Course'])

        # Adding model 'Meeting'
        db.create_table('courses_meeting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='meetings', to=orm['courses.Course'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('courses', ['Meeting'])

        # Adding M2M table for field readings on 'Meeting'
        db.create_table('courses_meeting_readings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm['courses.meeting'], null=False)),
            ('reading', models.ForeignKey(orm['courses.reading'], null=False))
        ))
        db.create_unique('courses_meeting_readings', ['meeting_id', 'reading_id'])

        # Adding model 'Reading'
        db.create_table('courses_reading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bibtex', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('courses', ['Reading'])


    def backwards(self, orm):
        
        # Deleting model 'Department'
        db.delete_table('courses_department')

        # Deleting model 'Course'
        db.delete_table('courses_course')

        # Deleting model 'Meeting'
        db.delete_table('courses_meeting')

        # Removing M2M table for field readings on 'Meeting'
        db.delete_table('courses_meeting_readings')

        # Deleting model 'Reading'
        db.delete_table('courses_reading')


    models = {
        'courses.course': {
            'Meta': {'object_name': 'Course'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': "orm['courses.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'semester': ('django.db.models.fields.IntegerField', [], {}),
            'times': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'courses.department': {
            'Meta': {'object_name': 'Department'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'courses.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meetings'", 'to': "orm['courses.Course']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'readings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['courses.Reading']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'courses.reading': {
            'Meta': {'object_name': 'Reading'},
            'bibtex': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['courses']
