# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'AbTest.default'
        db.delete_column('common_abtest', 'default_id')


    def backwards(self, orm):
        
        # Adding field 'AbTest.default'
        db.add_column('common_abtest', 'default', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='test', to=orm['common.AbTestCode']), keep_default=False)


    models = {
        'common.abtest': {
            'Meta': {'object_name': 'AbTest'},
            'code_choices': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'abtest'", 'symmetrical': 'False', 'to': "orm['common.AbTestCode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'common.abtestcode': {
            'Meta': {'object_name': 'AbTestCode'},
            'aff_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'code': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'common.blackfriday': {
            'Meta': {'object_name': 'BlackFriday'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.linxcontext': {
            'Meta': {'object_name': 'LinxContext'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'rin': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'common.spuncontent': {
            'Meta': {'object_name': 'SpunContent'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['common']
