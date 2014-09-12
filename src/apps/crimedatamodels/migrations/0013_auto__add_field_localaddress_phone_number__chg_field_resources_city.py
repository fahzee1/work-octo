# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'LocalAddress.phone_number'
        db.add_column('crimedatamodels_localaddress', 'phone_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Changing field 'Resources.city'
        db.alter_column('crimedatamodels_resources', 'city_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crimedatamodels.CityLocation'], null=True))


    def backwards(self, orm):
        
        # Deleting field 'LocalAddress.phone_number'
        db.delete_column('crimedatamodels_localaddress', 'phone_number')

        # Changing field 'Resources.city'
        db.alter_column('crimedatamodels_resources', 'city_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['crimedatamodels.CityLocation']))


    models = {
        'crimedatamodels.citycompetitor': {
            'Meta': {'object_name': 'CityCompetitor'},
            'alarm_monitoring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crimedatamodels.CityLocation']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'door_window': ('django.db.models.fields.CharField', [], {'default': "'3'", 'max_length': '255'}),
            'free_equipment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly_cost': ('django.db.models.fields.CharField', [], {'default': "'19.99'", 'max_length': '255'}),
            'no_fees': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rival': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'warranty': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'crimedatamodels.citycrimestats': {
            'Meta': {'unique_together': "(('city', 'year'),)", 'object_name': 'CityCrimeStats', 'db_table': "'city_crime_stats'"},
            'aggravated_assault_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'aggravated_assault_rank_per100k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'arson_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'arson_rank_per100k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'burglary_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'burglary_rank_per100k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['crimedatamodels.CrimesByCity']"}),
            'forcible_rape_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'forcible_rape_rank_per100k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'larceny_theft_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'larceny_theft_rank_per100k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'motor_vehicle_theft_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'motor_vehicle_theft_rank_per100k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'murder_and_nonnegligent_manslaughter_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'murder_and_nonnegligent_manslaughter_rank_per100k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'property_crime_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'property_crime_rank_per100k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'robbery_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'robbery_rank_per100k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'violent_crime_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'violent_crime_rank_per100k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'crimedatamodels.citylocation': {
            'Meta': {'ordering': "['state']", 'unique_together': "(('city_name', 'state'),)", 'object_name': 'CityLocation', 'db_table': "'citylocations'"},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'city_name_slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6', 'db_index': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'crimedatamodels.crimecontent': {
            'Meta': {'object_name': 'CrimeContent'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'population_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'crimedatamodels.crimesbycity': {
            'Meta': {'unique_together': "(('fbi_city_name', 'fbi_state', 'year'),)", 'object_name': 'CrimesByCity', 'db_table': "'crimes_by_city'"},
            'aggravated_assault': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'arson': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'burglary': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fbi_city_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'fbi_state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'forcible_rape': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'larceny_theft': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'motor_vehicle_theft': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'murder_and_nonnegligent_manslaughter': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'property_crime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'robbery': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'violent_crime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'crimedatamodels.featuredicon': {
            'Meta': {'object_name': 'FeaturedIcon'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crimedatamodels.CityLocation']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_height': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_width': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'crimedatamodels.featuredvideo': {
            'Meta': {'object_name': 'FeaturedVideo'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crimedatamodels.CityLocation']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video_embed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'crimedatamodels.localaddress': {
            'Meta': {'object_name': 'LocalAddress'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'googleplus_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        'crimedatamodels.matchaddresslocation': {
            'Meta': {'object_name': 'MatchAddressLocation'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crimedatamodels.LocalAddress']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crimedatamodels.CityLocation']"})
        },
        'crimedatamodels.resources': {
            'Meta': {'object_name': 'Resources'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crimedatamodels.CityLocation']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crimedatamodels.State']"}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'crimedatamodels.state': {
            'Meta': {'object_name': 'State', 'db_table': "'states'"},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        'crimedatamodels.statecrimestats': {
            'Meta': {'unique_together': "(('state', 'year'),)", 'object_name': 'StateCrimeStats', 'db_table': "'state_crime_stats'"},
            'aggravated_assault': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'aggravated_assault_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'aggravated_assault_rank_per100k': ('django.db.models.fields.IntegerField', [], {}),
            'arson': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'arson_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'arson_rank_per100k': ('django.db.models.fields.IntegerField', [], {}),
            'burglary': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'burglary_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'burglary_rank_per100k': ('django.db.models.fields.IntegerField', [], {}),
            'forcible_rape': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'forcible_rape_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'forcible_rape_rank_per100k': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'larceny_theft': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'larceny_theft_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'larceny_theft_rank_per100k': ('django.db.models.fields.IntegerField', [], {}),
            'motor_vehicle_theft': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'motor_vehicle_theft_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'motor_vehicle_theft_rank_per100k': ('django.db.models.fields.IntegerField', [], {}),
            'murder_and_nonnegligent_manslaughter': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'murder_and_nonnegligent_manslaughter_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'murder_and_nonnegligent_manslaughter_rank_per100k': ('django.db.models.fields.IntegerField', [], {}),
            'number_of_cities': ('django.db.models.fields.IntegerField', [], {}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'property_crime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'property_crime_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'property_crime_rank_per100k': ('django.db.models.fields.IntegerField', [], {}),
            'robbery': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'robbery_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'robbery_rank_per100k': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crimedatamodels.State']"}),
            'violent_crime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'violent_crime_grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'violent_crime_rank_per100k': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'crimedatamodels.zipcode': {
            'Meta': {'object_name': 'ZipCode', 'db_table': "'zip_codes'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6', 'db_index': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'zip': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5', 'primary_key': 'True'})
        }
    }

    complete_apps = ['crimedatamodels']
