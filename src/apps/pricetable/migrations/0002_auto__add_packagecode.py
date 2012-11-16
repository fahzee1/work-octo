# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PackageCode'
        db.create_table('pricetable_packagecode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('cart', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('pricetable', ['PackageCode'])


    def backwards(self, orm):
        
        # Deleting model 'PackageCode'
        db.delete_table('pricetable_packagecode')


    models = {
        'pricetable.package': {
            'Meta': {'object_name': 'Package'},
            'adt_monitoring': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'adt_upfront': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'broadband_monitoring': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'cellular_interactive_monitoring': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'cellular_monitoring': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landline_monitoring': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'standard_monitoring': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'upfront': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'pricetable.packagecode': {
            'Meta': {'object_name': 'PackageCode'},
            'cart': ('django.db.models.fields.TextField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['pricetable']
