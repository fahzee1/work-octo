# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Campaign'
        db.create_table('adspace_campaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=64, db_index=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('adspace', ['Campaign'])

        # Adding model 'Ad'
        db.create_table('adspace_ad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adspace.Campaign'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('sub_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('ad', self.gf('django.db.models.fields.FilePathField')(path='/Users/robert/Sites/proam/protectamerica/src/templates/adspace/', max_length=100, recursive=True)),
        ))
        db.send_create_signal('adspace', ['Ad'])


    def backwards(self, orm):
        
        # Deleting model 'Campaign'
        db.delete_table('adspace_campaign')

        # Deleting model 'Ad'
        db.delete_table('adspace_ad')


    models = {
        'adspace.ad': {
            'Meta': {'object_name': 'Ad'},
            'ad': ('django.db.models.fields.FilePathField', [], {'path': "'/Users/robert/Sites/proam/protectamerica/src/templates/adspace/'", 'max_length': '100', 'recursive': 'True'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adspace.Campaign']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '48'})
        },
        'adspace.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['adspace']
