# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Affiliate'
        db.create_table('affiliates_affiliate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agent_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('use_call_measurement', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('affiliates', ['Affiliate'])

        # Adding model 'AffTemplate'
        db.create_table('affiliates_afftemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('folder', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('affiliates', ['AffTemplate'])

        # Adding model 'LandingPage'
        db.create_table('affiliates_landingpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('affiliate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['affiliates.Affiliate'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['affiliates.AffTemplate'])),
        ))
        db.send_create_signal('affiliates', ['LandingPage'])

        # Adding model 'Profile'
        db.create_table('affiliates_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('taxid', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=10)),
            ('affiliate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['affiliates.Affiliate'], null=True, blank=True)),
        ))
        db.send_create_signal('affiliates', ['Profile'])


    def backwards(self, orm):
        
        # Deleting model 'Affiliate'
        db.delete_table('affiliates_affiliate')

        # Deleting model 'AffTemplate'
        db.delete_table('affiliates_afftemplate')

        # Deleting model 'LandingPage'
        db.delete_table('affiliates_landingpage')

        # Deleting model 'Profile'
        db.delete_table('affiliates_profile')


    models = {
        'affiliates.affiliate': {
            'Meta': {'object_name': 'Affiliate'},
            'agent_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'use_call_measurement': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'affiliates.afftemplate': {
            'Meta': {'object_name': 'AffTemplate'},
            'folder': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'affiliates.landingpage': {
            'Meta': {'object_name': 'LandingPage'},
            'affiliate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['affiliates.Affiliate']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['affiliates.AffTemplate']"})
        },
        'affiliates.profile': {
            'Meta': {'object_name': 'Profile'},
            'affiliate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['affiliates.Affiliate']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '10'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'taxid': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['affiliates']
