# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Affiliate.conversion_pixels'
        db.add_column('affiliates_affiliate', 'conversion_pixels', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Affiliate.conversion_pixels'
        db.delete_column('affiliates_affiliate', 'conversion_pixels')


    models = {
        'affiliates.affiliate': {
            'Meta': {'object_name': 'Affiliate'},
            'agent_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'conversion_pixels': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'homesite_override': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'pixels': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'thank_you': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
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
