# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MovingKit'
        db.create_table('contact_movingkit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            ('current_phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('current_city', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('current_state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2)),
            ('current_address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('current_zipcode', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('new_phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('new_city', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('new_state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
            ('new_address', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('new_zipcode', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('send_to_current_address', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('shipping_city', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('shipping_state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
            ('shipping_address', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('shipping_zipcode', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('contact', ['MovingKit'])

        # Adding field 'ContactUs.date_created'
        db.add_column('contact_contactus', 'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime.today(), blank=True), keep_default=False)

        # Adding field 'CEOFeedback.date_created'
        db.add_column('contact_ceofeedback', 'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime.today(), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'MovingKit'
        db.delete_table('contact_movingkit')

        # Deleting field 'ContactUs.date_created'
        db.delete_column('contact_contactus', 'date_created')

        # Deleting field 'CEOFeedback.date_created'
        db.delete_column('contact_ceofeedback', 'date_created')


    models = {
        'contact.ceofeedback': {
            'Meta': {'object_name': 'CEOFeedback'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'feedback_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'rep_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'contact.contactus': {
            'Meta': {'object_name': 'ContactUs'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'})
        },
        'contact.movingkit': {
            'Meta': {'object_name': 'MovingKit'},
            'current_address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'current_city': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'current_phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'current_state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'current_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'new_address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'new_city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'new_phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'new_state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'new_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'send_to_current_address': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'shipping_address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'shipping_city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'shipping_state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'shipping_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'})
        },
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
