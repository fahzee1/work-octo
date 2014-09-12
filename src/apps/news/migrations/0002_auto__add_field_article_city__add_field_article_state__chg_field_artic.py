# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Article.city'
        db.add_column('news_article', 'city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crimedatamodels.CityLocation'], null=True, blank=True), keep_default=False)

        # Adding field 'Article.state'
        db.add_column('news_article', 'state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crimedatamodels.State'], null=True, blank=True), keep_default=False)

        # Changing field 'Article.image'
        db.alter_column('news_article', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=256, null=True))


    def backwards(self, orm):
        
        # Deleting field 'Article.city'
        db.delete_column('news_article', 'city_id')

        # Deleting field 'Article.state'
        db.delete_column('news_article', 'state_id')

        # Changing field 'Article.image'
        db.alter_column('news_article', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))


    models = {
        'crimedatamodels.citylocation': {
            'Meta': {'ordering': "['state']", 'unique_together': "(('city_name', 'state'),)", 'object_name': 'CityLocation', 'db_table': "'citylocations'"},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'city_name_slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6', 'db_index': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'crimedatamodels.state': {
            'Meta': {'object_name': 'State', 'db_table': "'states'"},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        'news.article': {
            'Meta': {'object_name': 'Article'},
            'brafton_id': ('django.db.models.fields.IntegerField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['news.Category']", 'symmetrical': 'False'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crimedatamodels.CityLocation']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'image_caption': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crimedatamodels.State']", 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {})
        },
        'news.category': {
            'Meta': {'object_name': 'Category'},
            'brafton_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['news']
