# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Talk.subtitle'
        db.add_column('talking_talk', 'subtitle', self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Talk.subtitle'
        db.delete_column('talking_talk', 'subtitle')


    models = {
        'talking.talk': {
            'Meta': {'object_name': 'Talk'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'embed': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80', 'db_index': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['talking']
