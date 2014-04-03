# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'TweetBackup', fields ['text']
        db.create_unique('newsfeed_tweetbackup', ['text'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'TweetBackup', fields ['text']
        db.delete_unique('newsfeed_tweetbackup', ['text'])


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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 3, 11, 21, 55, 463412)', 'auto_now_add': 'True', 'blank': 'True'}),
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 3, 11, 21, 55, 464375)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payitfoward': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['newsfeed']
