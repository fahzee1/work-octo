# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'KeywordMatch'
        db.create_table('search_keywordmatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('page', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('search', ['KeywordMatch'])


    def backwards(self, orm):
        
        # Deleting model 'KeywordMatch'
        db.delete_table('search_keywordmatch')


    models = {
        'search.keywordmatch': {
            'Meta': {'object_name': 'KeywordMatch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['search']
