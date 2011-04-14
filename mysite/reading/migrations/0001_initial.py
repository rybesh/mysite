# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Text'
        db.create_table('reading_text', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('bibtex', self.gf('django.db.models.fields.TextField')()),
            ('markdown', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('citation_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('reading', ['Text'])

        # Adding M2M table for field related_texts on 'Text'
        db.create_table('reading_text_related_texts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_text', models.ForeignKey(orm['reading.text'], null=False)),
            ('to_text', models.ForeignKey(orm['reading.text'], null=False))
        ))
        db.create_unique('reading_text_related_texts', ['from_text_id', 'to_text_id'])

        # Adding model 'Note'
        db.create_table('reading_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reading.Text'])),
            ('markdown', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(unique=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('reading', ['Note'])


    def backwards(self, orm):
        
        # Deleting model 'Text'
        db.delete_table('reading_text')

        # Removing M2M table for field related_texts on 'Text'
        db.delete_table('reading_text_related_texts')

        # Deleting model 'Note'
        db.delete_table('reading_note')


    models = {
        'reading.note': {
            'Meta': {'object_name': 'Note'},
            'created': ('django.db.models.fields.DateTimeField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markdown': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'text': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reading.Text']"})
        },
        'reading.text': {
            'Meta': {'object_name': 'Text'},
            'bibtex': ('django.db.models.fields.TextField', [], {}),
            'citation_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'markdown': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'related_texts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_texts_rel_+'", 'to': "orm['reading.Text']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['reading']
