# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Venue'
        db.create_table('events_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('events', ['Venue'])

        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Venue'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('event_url', self.gf('django.db.models.fields.CharField')(default=u'', max_length=500, blank=True)),
            ('eventdate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('eventstart', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('eventfinish', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('events', ['Event'])


    def backwards(self, orm):
        
        # Deleting model 'Venue'
        db.delete_table('events_venue')

        # Deleting model 'Event'
        db.delete_table('events_event')


    models = {
        'events.event': {
            'Meta': {'ordering': "['eventdate', 'eventstart']", 'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_url': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '500', 'blank': 'True'}),
            'eventdate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'eventfinish': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'eventstart': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Venue']"})
        },
        'events.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['events']
