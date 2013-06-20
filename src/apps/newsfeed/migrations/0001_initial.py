# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DateFeed'
        db.create_table('newsfeed_datefeed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('newsfeed', ['DateFeed'])

        # Adding model 'FeedType'
        db.create_table('newsfeed_feedtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('newsfeed', ['FeedType'])

        # Adding model 'NewsFeed'
        db.create_table('newsfeed_newsfeed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='Choose State', max_length=2, null=True, blank=True)),
            ('date_feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsfeed.DateFeed'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsfeed.FeedType'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 20, 17, 2, 1, 496354), auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('newsfeed', ['NewsFeed'])


    def backwards(self, orm):
        
        # Deleting model 'DateFeed'
        db.delete_table('newsfeed_datefeed')

        # Deleting model 'FeedType'
        db.delete_table('newsfeed_feedtype')

        # Deleting model 'NewsFeed'
        db.delete_table('newsfeed_newsfeed')


    models = {
        'newsfeed.datefeed': {
            'Meta': {'object_name': 'DateFeed'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'newsfeed.feedtype': {
            'Meta': {'object_name': 'FeedType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'newsfeed.newsfeed': {
            'Meta': {'object_name': 'NewsFeed'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 20, 17, 2, 1, 496354)', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsfeed.DateFeed']"}),
            'expires': ('django.db.models.fields.DateField', [], {}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'Choose State'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsfeed.FeedType']"})
        }
    }

    complete_apps = ['newsfeed']
