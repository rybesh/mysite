# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Talk'
        db.create_table('talking_talk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=80, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('embed', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('talking', ['Talk'])


    def backwards(self, orm):
        
        # Deleting model 'Talk'
        db.delete_table('talking_talk')


    models = {
        'talking.talk': {
            'Meta': {'object_name': 'Talk'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'embed': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['talking']
