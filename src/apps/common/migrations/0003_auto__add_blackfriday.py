# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BlackFriday'
        db.create_table('common_blackfriday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['BlackFriday'])


    def backwards(self, orm):
        
        # Deleting model 'BlackFriday'
        db.delete_table('common_blackfriday')


    models = {
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
