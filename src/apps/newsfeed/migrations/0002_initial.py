# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AddDate'
        db.create_table('newsfeed_adddate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('newsfeed', ['AddDate'])

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
            ('state', self.gf('django.db.models.fields.CharField')(default='Choose State', max_length=2, null=True, blank=True)),
            ('date_feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsfeed.AddDate'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsfeed.AddType'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 8, 26, 43, 796455), auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('newsfeed', ['TheFeed'])


    def backwards(self, orm):
        
        # Deleting model 'AddDate'
        db.delete_table('newsfeed_adddate')

        # Deleting model 'AddType'
        db.delete_table('newsfeed_addtype')

        # Deleting model 'TheFeed'
        db.delete_table('newsfeed_thefeed')


    models = {
        'newsfeed.adddate': {
            'Meta': {'object_name': 'AddDate'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 8, 26, 43, 796455)', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsfeed.AddDate']"}),
            'expires': ('django.db.models.fields.DateField', [], {}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'Choose State'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsfeed.AddType']"})
        }
    }

    complete_apps = ['newsfeed']
