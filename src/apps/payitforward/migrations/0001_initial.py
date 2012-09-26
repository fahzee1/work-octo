# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Organization'
        db.create_table('payitforward_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('color', self.gf('colorful.fields.RGBColorField')(max_length=7)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('payitforward', ['Organization'])

        # Adding model 'Points'
        db.create_table('payitforward_points', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payitforward.Organization'])),
        ))
        db.send_create_signal('payitforward', ['Points'])


    def backwards(self, orm):
        
        # Deleting model 'Organization'
        db.delete_table('payitforward_organization')

        # Deleting model 'Points'
        db.delete_table('payitforward_points')


    models = {
        'payitforward.organization': {
            'Meta': {'object_name': 'Organization'},
            'color': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'payitforward.points': {
            'Meta': {'object_name': 'Points'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['payitforward.Organization']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        }
    }

    complete_apps = ['payitforward']
