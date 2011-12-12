# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Testimonial'
        db.create_table('testimonials_testimonial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('experience', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('rep', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('can_post', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('testimonial', self.gf('django.db.models.fields.TextField')()),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('testimonials', ['Testimonial'])


    def backwards(self, orm):
        
        # Deleting model 'Testimonial'
        db.delete_table('testimonials_testimonial')


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
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'rep': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'testimonial': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['testimonials']
