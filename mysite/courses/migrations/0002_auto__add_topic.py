# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Topic'
        db.create_table('courses_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('courses', ['Topic'])

        # Adding M2M table for field topics on 'Meeting'
        db.create_table('courses_meeting_topics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm['courses.meeting'], null=False)),
            ('topic', models.ForeignKey(orm['courses.topic'], null=False))
        ))
        db.create_unique('courses_meeting_topics', ['meeting_id', 'topic_id'])


    def backwards(self, orm):
        
        # Deleting model 'Topic'
        db.delete_table('courses_topic')

        # Removing M2M table for field topics on 'Meeting'
        db.delete_table('courses_meeting_topics')


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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['courses.Topic']", 'symmetrical': 'False'})
        },
        'courses.reading': {
            'Meta': {'object_name': 'Reading'},
            'bibtex': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'courses.topic': {
            'Meta': {'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['courses']
