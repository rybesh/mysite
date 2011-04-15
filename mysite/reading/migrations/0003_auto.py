# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'Note', fields ['created']
        db.create_index('reading_note', ['created'])

        # Adding index on 'Text', fields ['citation_key']
        db.create_index('reading_text', ['citation_key'])


    def backwards(self, orm):
        
        # Removing index on 'Text', fields ['citation_key']
        db.delete_index('reading_text', ['citation_key'])

        # Removing index on 'Note', fields ['created']
        db.delete_index('reading_note', ['created'])


    models = {
        'reading.note': {
            'Meta': {'object_name': 'Note'},
            'created': ('django.db.models.fields.DateTimeField', [], {'unique': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markdown': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'text': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reading.Text']"})
        },
        'reading.text': {
            'Meta': {'object_name': 'Text'},
            'bibtex': ('django.db.models.fields.TextField', [], {}),
            'citation_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'markdown': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'related_texts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_texts_rel_+'", 'to': "orm['reading.Text']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['reading']
