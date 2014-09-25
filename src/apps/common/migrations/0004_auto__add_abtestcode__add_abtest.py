# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AbTestCode'
        db.create_table('common_abtestcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('aff_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('common', ['AbTestCode'])

        # Adding model 'AbTest'
        db.create_table('common_abtest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('common', ['AbTest'])

        # Adding M2M table for field code_choices on 'AbTest'
        db.create_table('common_abtest_code_choices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('abtest', models.ForeignKey(orm['common.abtest'], null=False)),
            ('abtestcode', models.ForeignKey(orm['common.abtestcode'], null=False))
        ))
        db.create_unique('common_abtest_code_choices', ['abtest_id', 'abtestcode_id'])


    def backwards(self, orm):
        
        # Deleting model 'AbTestCode'
        db.delete_table('common_abtestcode')

        # Deleting model 'AbTest'
        db.delete_table('common_abtest')

        # Removing M2M table for field code_choices on 'AbTest'
        db.delete_table('common_abtest_code_choices')


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
