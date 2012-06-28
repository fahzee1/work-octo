# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Textimonial'
        db.create_table('testimonials_textimonial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('rating', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('permission_to_post', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('testimonials', ['Textimonial'])

        # Changing field 'Testimonial.last_name'
        db.alter_column('testimonials_testimonial', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=36, null=True))


    def backwards(self, orm):
        
        # Deleting model 'Textimonial'
        db.delete_table('testimonials_textimonial')

        # Changing field 'Testimonial.last_name'
        db.alter_column('testimonials_testimonial', 'last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=36))


    models = {
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'permission_to_post': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rating': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['testimonials']
