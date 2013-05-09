# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Package'
        db.create_table('pricetable_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('upfront', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('adt_upfront', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('adt_monitoring', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('standard_monitoring', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('landline_monitoring', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('broadband_monitoring', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('cellular_monitoring', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('cellular_interactive_monitoring', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('pricetable', ['Package'])


    def backwards(self, orm):
        
        # Deleting model 'Package'
        db.delete_table('pricetable_package')


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
        }
    }

    complete_apps = ['pricetable']
