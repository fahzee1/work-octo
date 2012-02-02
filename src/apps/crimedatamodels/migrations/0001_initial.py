# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ZipCode'
        db.create_table('zip_codes', (
            ('zip', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5, primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6, db_index=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6, db_index=True)),
        ))
        db.send_create_signal('crimedatamodels', ['ZipCode'])

        # Adding model 'State'
        db.create_table('states', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
        ))
        db.send_create_signal('crimedatamodels', ['State'])

        # Adding model 'CityLocation'
        db.create_table('citylocations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6, db_index=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6, db_index=True)),
        ))
        db.send_create_signal('crimedatamodels', ['CityLocation'])

        # Adding unique constraint on 'CityLocation', fields ['city_name', 'state']
        db.create_unique('citylocations', ['city_name', 'state'])

        # Adding model 'CrimesByCity'
        db.create_table('crimes_by_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fbi_city_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('fbi_state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('population', self.gf('django.db.models.fields.IntegerField')()),
            ('aggravated_assault', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('arson', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('burglary', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('forcible_rape', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('larceny_theft', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('motor_vehicle_theft', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('murder_and_nonnegligent_manslaughter', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('property_crime', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('robbery', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('violent_crime', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('crimedatamodels', ['CrimesByCity'])

        # Adding unique constraint on 'CrimesByCity', fields ['fbi_city_name', 'fbi_state', 'year']
        db.create_unique('crimes_by_city', ['fbi_city_name', 'fbi_state', 'year'])

        # Adding model 'CityCrimeStats'
        db.create_table('city_crime_stats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats', to=orm['crimedatamodels.CrimesByCity'])),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('aggravated_assault_rank_per100k', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('arson_rank_per100k', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('burglary_rank_per100k', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('forcible_rape_rank_per100k', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('larceny_theft_rank_per100k', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('motor_vehicle_theft_rank_per100k', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('murder_and_nonnegligent_manslaughter_rank_per100k', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('property_crime_rank_per100k', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('robbery_rank_per100k', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('violent_crime_rank_per100k', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('aggravated_assault_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('arson_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('burglary_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('forcible_rape_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('larceny_theft_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('motor_vehicle_theft_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('murder_and_nonnegligent_manslaughter_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('property_crime_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('robbery_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('violent_crime_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
        ))
        db.send_create_signal('crimedatamodels', ['CityCrimeStats'])

        # Adding unique constraint on 'CityCrimeStats', fields ['city', 'year']
        db.create_unique('city_crime_stats', ['city_id', 'year'])

        # Adding model 'StateCrimeStats'
        db.create_table('state_crime_stats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crimedatamodels.State'])),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('number_of_cities', self.gf('django.db.models.fields.IntegerField')()),
            ('population', self.gf('django.db.models.fields.IntegerField')()),
            ('aggravated_assault', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('arson', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('burglary', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('forcible_rape', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('larceny_theft', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('motor_vehicle_theft', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('murder_and_nonnegligent_manslaughter', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('property_crime', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('robbery', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('violent_crime', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('aggravated_assault_rank_per100k', self.gf('django.db.models.fields.IntegerField')()),
            ('arson_rank_per100k', self.gf('django.db.models.fields.IntegerField')()),
            ('burglary_rank_per100k', self.gf('django.db.models.fields.IntegerField')()),
            ('forcible_rape_rank_per100k', self.gf('django.db.models.fields.IntegerField')()),
            ('larceny_theft_rank_per100k', self.gf('django.db.models.fields.IntegerField')()),
            ('motor_vehicle_theft_rank_per100k', self.gf('django.db.models.fields.IntegerField')()),
            ('murder_and_nonnegligent_manslaughter_rank_per100k', self.gf('django.db.models.fields.IntegerField')()),
            ('property_crime_rank_per100k', self.gf('django.db.models.fields.IntegerField')()),
            ('robbery_rank_per100k', self.gf('django.db.models.fields.IntegerField')()),
            ('violent_crime_rank_per100k', self.gf('django.db.models.fields.IntegerField')()),
            ('aggravated_assault_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('arson_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('burglary_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('forcible_rape_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('larceny_theft_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('motor_vehicle_theft_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('murder_and_nonnegligent_manslaughter_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('property_crime_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('robbery_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('violent_crime_grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
        ))
        db.send_create_signal('crimedatamodels', ['StateCrimeStats'])

        # Adding unique constraint on 'StateCrimeStats', fields ['state', 'year']
        db.create_unique('state_crime_stats', ['state_id', 'year'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'StateCrimeStats', fields ['state', 'year']
        db.delete_unique('state_crime_stats', ['state_id', 'year'])

        # Removing unique constraint on 'CityCrimeStats', fields ['city', 'year']
        db.delete_unique('city_crime_stats', ['city_id', 'year'])

        # Removing unique constraint on 'CrimesByCity', fields ['fbi_city_name', 'fbi_state', 'year']
        db.delete_unique('crimes_by_city', ['fbi_city_name', 'fbi_state', 'year'])

        # Removing unique constraint on 'CityLocation', fields ['city_name', 'state']
        db.delete_unique('citylocations', ['city_name', 'state'])

        # Deleting model 'ZipCode'
        db.delete_table('zip_codes')

        # Deleting model 'State'
        db.delete_table('states')

        # Deleting model 'CityLocation'
        db.delete_table('citylocations')

        # Deleting model 'CrimesByCity'
        db.delete_table('crimes_by_city')

        # Deleting model 'CityCrimeStats'
        db.delete_table('city_crime_stats')

        # Deleting model 'StateCrimeStats'
        db.delete_table('state_crime_stats')


    models = {
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
            'Meta': {'unique_together': "(('city_name', 'state'),)", 'object_name': 'CityLocation', 'db_table': "'citylocations'"},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6', 'db_index': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
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
        'crimedatamodels.state': {
            'Meta': {'object_name': 'State', 'db_table': "'states'"},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
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
            'population': ('django.db.models.fields.IntegerField', [], {}),
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
