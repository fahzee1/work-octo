# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Ad.inline_styles'
        db.add_column('adspace_ad', 'inline_styles', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Ad.inline_styles'
        db.delete_column('adspace_ad', 'inline_styles')


    models = {
        'adspace.ad': {
            'Meta': {'object_name': 'Ad'},
            'ad': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adspace.Campaign']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'element_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inline_styles': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sub_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'adspace.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['adspace']
