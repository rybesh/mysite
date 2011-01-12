# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Assignment'
        db.create_table('courses_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignments', to=orm['courses.Course'])),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('courses', ['Assignment'])


    def backwards(self, orm):
        
        # Deleting model 'Assignment'
        db.delete_table('courses_assignment')


    models = {
        'courses.assignment': {
            'Meta': {'ordering': "('due_date',)", 'object_name': 'Assignment'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['courses.Course']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'courses.course': {
            'Meta': {'unique_together': "(('slug', 'semester', 'year'),)", 'object_name': 'Course'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': "orm['courses.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': "orm['courses.Instructor']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
        'courses.holiday': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Holiday'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'holidays'", 'to': "orm['courses.Course']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'courses.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'office_hours': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '14'})
        },
        'courses.meeting': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Meeting'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meetings'", 'to': "orm['courses.Course']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_tentative': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'readings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['courses.Reading']", 'symmetrical': 'False', 'through': "orm['courses.ReadingAssignment']", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['courses.Topic']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'courses.reading': {
            'Meta': {'ordering': "('citekey',)", 'object_name': 'Reading'},
            'bibtex': ('django.db.models.fields.TextField', [], {}),
            'citekey': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'courses.readingassignment': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ReadingAssignment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Meeting']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reading': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Reading']"})
        },
        'courses.topic': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['courses']
