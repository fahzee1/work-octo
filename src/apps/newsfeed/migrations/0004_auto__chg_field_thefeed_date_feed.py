# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'TheFeed.date_feed'
        db.alter_column('newsfeed_thefeed', 'date_feed_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsfeed.AddDate'], null=True))


    def backwards(self, orm):
        
        # Changing field 'TheFeed.date_feed'
        db.alter_column('newsfeed_thefeed', 'date_feed_id', self.gf('django.db.models.fields.related.ForeignKey')(default=datetime.date(2013, 6, 21), to=orm['newsfeed.AddDate']))


    models = {
        'newsfeed.adddate': {
            'Meta': {'object_name': 'AddDate'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'newsfeed.addtype': {
            'Meta': {'object_name': 'AddType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'newsfeed.thefeed': {
            'Meta': {'object_name': 'TheFeed'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 8, 39, 26, 430075)', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsfeed.AddDate']", 'null': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsfeed.AddType']"})
        }
    }

    complete_apps = ['newsfeed']
