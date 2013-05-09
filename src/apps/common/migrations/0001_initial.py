# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SpunContent'
        db.create_table('common_spuncontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('common', ['SpunContent'])


    def backwards(self, orm):
        
        # Deleting model 'SpunContent'
        db.delete_table('common_spuncontent')


    models = {
        'common.spuncontent': {
            'Meta': {'object_name': 'SpunContent'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['common']
