# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Meeting.is_tentative'
        db.add_column('courses_meeting', 'is_tentative', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Meeting.is_tentative'
        db.delete_column('courses_meeting', 'is_tentative')


    models = {
        'courses.course': {
            'Meta': {'unique_together': "(('slug', 'semester', 'year'),)", 'object_name': 'Course'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': "orm['courses.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
