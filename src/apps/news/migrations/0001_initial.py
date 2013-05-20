# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('news_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('brafton_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('news', ['Category'])

        # Adding model 'Article'
        db.create_table('news_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brafton_id', self.gf('django.db.models.fields.IntegerField')()),
            ('heading', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image_caption', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('news', ['Article'])

        # Adding M2M table for field categories on 'Article'
        db.create_table('news_article_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['news.article'], null=False)),
            ('category', models.ForeignKey(orm['news.category'], null=False))
        ))
        db.create_unique('news_article_categories', ['article_id', 'category_id'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('news_category')

        # Deleting model 'Article'
        db.delete_table('news_article')

        # Removing M2M table for field categories on 'Article'
        db.delete_table('news_article_categories')


    models = {
        'news.article': {
            'Meta': {'object_name': 'Article'},
            'brafton_id': ('django.db.models.fields.IntegerField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['news.Category']", 'symmetrical': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_caption': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
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
