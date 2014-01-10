# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'TweetBackup.location'
        db.add_column('newsfeed_tweetbackup', 'location', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'TweetBackup.location'
        db.delete_column('newsfeed_tweetbackup', 'location')


    models = {
        'newsfeed.addtype': {
            'Meta': {'object_name': 'AddType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'newsfeed.fallbacks': {
            'Meta': {'object_name': 'FallBacks'},
            'feed_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsfeed.TheFeed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'newsfeed.thefeed': {
            'Meta': {'object_name': 'TheFeed'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 3, 12, 23, 47, 458052)', 'auto_now_add': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsfeed.AddType']"}),
            'visible_to_all': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'newsfeed.tweetbackup': {
            'GetRelativeCreatedAt': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'TweetBackup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 3, 12, 23, 47, 458893)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'payitfoward': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['newsfeed']
