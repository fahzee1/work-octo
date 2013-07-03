# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AddType'
        db.create_table('newsfeed_addtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('newsfeed', ['AddType'])

        # Adding model 'TheFeed'
        db.create_table('newsfeed_thefeed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('link_name', self.gf('django.db.models.fields.CharField')(default='Click Here', max_length=255, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsfeed.AddType'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 2, 15, 35, 56, 329967), auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('newsfeed', ['TheFeed'])

        # Adding model 'FallBacks'
        db.create_table('newsfeed_fallbacks', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsfeed.TheFeed'])),
        ))
        db.send_create_signal('newsfeed', ['FallBacks'])


    def backwards(self, orm):
        
        # Deleting model 'AddType'
        db.delete_table('newsfeed_addtype')

        # Deleting model 'TheFeed'
        db.delete_table('newsfeed_thefeed')

        # Deleting model 'FallBacks'
        db.delete_table('newsfeed_fallbacks')


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
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 15, 35, 56, 329967)', 'auto_now_add': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_name': ('django.db.models.fields.CharField', [], {'default': "'Click Here'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsfeed.AddType']"})
        }
    }

    complete_apps = ['newsfeed']
