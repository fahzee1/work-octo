# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TextimonialCityCache'
        db.create_table('testimonials_textimonialcitycache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2)),
        ))
        db.send_create_signal('testimonials', ['TextimonialCityCache'])

        # Adding M2M table for field testimonials on 'TextimonialCityCache'
        db.create_table('testimonials_textimonialcitycache_testimonials', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('textimonialcitycache', models.ForeignKey(orm['testimonials.textimonialcitycache'], null=False)),
            ('textimonial', models.ForeignKey(orm['testimonials.textimonial'], null=False))
        ))
        db.create_unique('testimonials_textimonialcitycache_testimonials', ['textimonialcitycache_id', 'textimonial_id'])

        # Adding unique constraint on 'TextimonialCityCache', fields ['city', 'state']
        db.create_unique('testimonials_textimonialcitycache', ['city', 'state'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'TextimonialCityCache', fields ['city', 'state']
        db.delete_unique('testimonials_textimonialcitycache', ['city', 'state'])

        # Deleting model 'TextimonialCityCache'
        db.delete_table('testimonials_textimonialcitycache')

        # Removing M2M table for field testimonials on 'TextimonialCityCache'
        db.delete_table('testimonials_textimonialcitycache_testimonials')


    models = {
        'contact.ceofeedback': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'CEOFeedback'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'converted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_read': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'feedback_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'rating': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '4'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rep_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'testimonials.testimonial': {
            'Meta': {'object_name': 'Testimonial'},
            'can_post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'experience': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'rep': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'testimonial': ('django.db.models.fields.TextField', [], {})
        },
        'testimonials.textimonial': {
            'Meta': {'object_name': 'Textimonial'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'converted_from': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.CEOFeedback']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_read': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'permission_to_post': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rating': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'})
        },
        'testimonials.textimonialcitycache': {
            'Meta': {'unique_together': "(('city', 'state'),)", 'object_name': 'TextimonialCityCache'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'testimonials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['testimonials.Textimonial']", 'max_length': '4', 'symmetrical': 'False'})
        },
        'testimonials.vidimonial': {
            'Meta': {'object_name': 'Vidimonial'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video_url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['testimonials']
