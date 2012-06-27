# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'LinxContext'
        db.create_table('common_linxcontext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('rin', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('common', ['LinxContext'])


    def backwards(self, orm):
        
        # Deleting model 'LinxContext'
        db.delete_table('common_linxcontext')


    models = {
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
