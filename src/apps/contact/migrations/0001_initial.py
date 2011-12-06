# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Submission'
        db.create_table('contact_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            ('phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('package', self.gf('django.db.models.fields.CharField')(max_length=24, null=True, blank=True)),
            ('feedback_type', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('rep_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('homeowner', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('creditrating', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('consent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('referer_page', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('contact', ['Submission'])


    def backwards(self, orm):
        
        # Deleting model 'Submission'
        db.delete_table('contact_submission')


    models = {
        'contact.submission': {
            'Meta': {'object_name': 'Submission'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'consent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creditrating': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'feedback_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'homeowner': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'package': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'referer_page': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'rep_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['contact']
