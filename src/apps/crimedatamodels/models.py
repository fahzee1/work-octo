import re
import pdb
from django.core.urlresolvers import reverse
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum,Q
from django.template.defaultfilters import slugify
from geopy import geocoders

GRADE_MAP = {'F':1, 'D':2, 'C':3, 'B':4, 'A':5}


GRADE_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('F', 'F'),
)


POPULATION_TYPES = (
    ('TOWN', 'Town'),
    ('CITY', 'City'),
    ('METROPOLIS', 'Metropolis'),
)


class ZipCode(models.Model):
    zip = models.CharField(primary_key=True, max_length=5, unique=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,
        db_index=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,
        db_index=True)

    def __unicode__(self):
        return self.zip

    class Meta:
        db_table = 'zip_codes'


class State(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True)

    def __unicode__(self):
        return '%s %s' % (self.abbreviation, self.name)

    class Meta:
        db_table = 'states'

    def get_absolute_url(self):
        return reverse('crime-rate:choose-city', args=[self.abbreviation])


class CityLocation(models.Model):
    city_name = models.CharField(max_length=64)
    city_name_slug = models.SlugField(max_length=64)
    state = models.CharField(max_length=2)

    latitude = models.DecimalField(max_digits=10, decimal_places=6,
        db_index=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,
        db_index=True)

    class Meta:
        db_table = 'citylocations'
        unique_together = (('city_name', 'state'),)
        ordering=['state']

    def __unicode__(self):
        return '%s, %s' % (self.city_name, self.state)

    def get_absolute_url(self):
        return reverse('crime-rate:crime-stats', args=[self.state,
            self.city_name])

    def join_name(self,local=False):
        kv = {}
        slug = self.city_name_slug
        if "'" in self.city_name:
            kv['name'],kv['slug'] = slug.title(),slug 
            return kv

        names = self.city_name
        if '(' or ')' in names:
            names.replace('(','').replace(')','')
        names = names.split(' ')

        if len(names) == 1:
            name = self.city_name
            if local:
                kv['name'],kv['slug'] = name.lower(),slug
                return kv
            else:
                kv['name'],kv['slug'] = name,slug
                return kv
        elif len(names) == 2:
            if '.' in self.city_name:
                names=self.city_name.replace('.','').split(' ')
                if len(names) == 2:
                    first,second = names[0],names[1].lower()
                    kv['name'],kv['slug'] = first+second,slug
                    return kv
                if len(names) == 3:
                    first,second,third = names[0],names[1].lower(),names[2].lower()
                    kv['name'],kv['slug'] = first+second+third,slug
                    return kv
            first,second=names[0],names[1].lower()
            kv['name'],kv['slug'] = first+second,slug
            return kv
        elif len(names) == 3:
            first,second,third=names[0],names[1].lower(),names[2].lower()
            kv['name'],kv['slug'] = first+second+third,slug
            return kv
        elif len(names) == 4:
            first,second,third,fourth=names[0],names[1].lower(),names[2].lower(),names[3].lower()
            kv['name'],kv['slug'] = first+second+third+fourth,slug
            return kv
        elif len(names) == 5:
            first,second,third,fourth,fifth=names[0],names[1].lower(),names[2].lower(),names[3].lower(),names[4].lower()
            kv['name'],kv['slug'] = first+second+third+fourth+fifth,slug
            return kv
        else:
            pass


    @property
    def slug_name(self):
        return self.city_name.lower().replace(' ', '-')


class CrimesByCity(models.Model):
    fbi_city_name = models.CharField(max_length=64)
    fbi_state = models.CharField(max_length=2)
    year = models.IntegerField()
    population = models.IntegerField()
    aggravated_assault = models.IntegerField(null=True)
    arson = models.IntegerField(null=True)
    burglary = models.IntegerField(null=True)
    forcible_rape = models.IntegerField(null=True)
    larceny_theft = models.IntegerField(null=True)
    motor_vehicle_theft = models.IntegerField(null=True)
    murder_and_nonnegligent_manslaughter = models.IntegerField(null=True)
    property_crime = models.IntegerField(null=True)
    robbery = models.IntegerField(null=True)
    violent_crime = models.IntegerField(null=True)

    class Meta:
        db_table = 'crimes_by_city'
        unique_together = (('fbi_city_name', 'fbi_state', 'year'),)

    def __unicode__(self):
        return '%s %s, %s' % (self.year, self.fbi_city_name, self.fbi_state)

    def by_100k(self, field_name):
        """Get the requested field, but measured in per-100,000-population."""
        val = getattr(self, field_name)
        if val is None:
            return val
        return 1e5*val/max(1.0, self.population)


    def check_create_if_none(self):
        # run this multiple times cause most likely will run out of trys then throw an error
        # note had to run 5 times first time using script
        try:
            #try and get city location in DB
            city = CityLocation.objects.get(city_name_slug=slugify(self.fbi_city_name),state=self.fbi_state)
            return ' skipping city %s,%s is there' % (self.fbi_city_name,self.fbi_state)
        except CityLocation.DoesNotExist:
            #if not there create one (also using geocode to get latitude longitude)
            city_n = self.fbi_city_name
            state = self.fbi_state
            try:
                g = geocoders.GoogleV3()
                results = g.geocode(city_n+','+state,exactly_one=False)
                addr ,(lat,lng) = results[0]
            except:
                try:
                    g = geocoders.GeocoderDotUS()
                    results = g.geocode(city_n+','+state,exactly_one=False)
                    addr ,(lat,lng) = results[0]
                except:
                    try:
                        g = geocoders.GeoNames()
                        results = g.geocode(city_n+','+state,exactly_one=False)
                        addr ,(lat,lng) = results[0]
                    except:
                        try:
                            g = geocoders.MediaWiki("http://wiki.case.edu/%s")
                            results = g.geocode(city_n+','+state,exactly_one=False)
                            addr ,(lat,lng) = results[0]
                        except:
                            pass

            city = CityLocation.objects.create(city_name=city_n,city_name_slug=slugify(city_n),state=state,latitude=lat,longitude=lng)
            return 'created city %s, %s' % (city_n,state)
    








class CityCrimeStats(models.Model):
    """Volatile city crime stats computed from the CrimesByCity table.

    These stats are volatile--changing any data in CrimesByCity invalidates
    the correctness of this table. If you add new crime data, be sure to
    recompute this table's values.

    """
    city = models.ForeignKey(CrimesByCity, related_name='stats')
    year = models.IntegerField()
    aggravated_assault_rank_per100k = models.IntegerField(null=True)
    arson_rank_per100k = models.IntegerField(null=True)
    burglary_rank_per100k = models.IntegerField(null=True)
    forcible_rape_rank_per100k = models.IntegerField(null=True)
    larceny_theft_rank_per100k = models.IntegerField(null=True)
    motor_vehicle_theft_rank_per100k = models.IntegerField(null=True)
    murder_and_nonnegligent_manslaughter_rank_per100k = models.IntegerField(
        null=True)
    property_crime_rank_per100k = models.IntegerField(null=True)
    robbery_rank_per100k = models.IntegerField(null=True)
    violent_crime_rank_per100k = models.IntegerField(null=True)
    aggravated_assault_grade = models.CharField(null=True, max_length=1)
    arson_grade = models.CharField(null=True, max_length=1)
    burglary_grade = models.CharField(null=True, max_length=1)
    forcible_rape_grade = models.CharField(null=True, max_length=1)
    larceny_theft_grade = models.CharField(null=True, max_length=1)
    motor_vehicle_theft_grade = models.CharField(null=True, max_length=1)
    murder_and_nonnegligent_manslaughter_grade = models.CharField(null=True,
        max_length=1)
    property_crime_grade = models.CharField(null=True,
        max_length=1)
    robbery_grade = models.CharField(null=True,
        max_length=1)
    violent_crime_grade = models.CharField(null=True,
        max_length=1)

    class Meta:
        db_table = 'city_crime_stats'
        unique_together = (('city', 'year'),)

    def __unicode__(self):
        return "%s" % self.city
        
    @property
    def average_grade(self):

        def get_grade_or_None(grade):
            try:
                return GRADE_MAP[grade]
            except:
                return 0

        used_fields_for_avg = [
            get_grade_or_None(self.aggravated_assault_grade),
            get_grade_or_None(self.burglary_grade),
            get_grade_or_None(self.forcible_rape_grade),
            get_grade_or_None(self.larceny_theft_grade),
            get_grade_or_None(self.motor_vehicle_theft_grade),
            get_grade_or_None(self.murder_and_nonnegligent_manslaughter_grade),
            get_grade_or_None(self.robbery_grade),
        ]
        used_fields_for_avg = [x for x in used_fields_for_avg if x != 0]
        ag = int(round(float(sum(used_fields_for_avg)) / float(len(used_fields_for_avg))))
        return [k for k, v in GRADE_MAP.iteritems() if v == ag][0]




class StateCrimeStats(models.Model):
    """Volatile state crime stats computed from the CrimesByCity table.

    These stats are volatile--changing any data in CrimesByCity invalidates
    the correctness of this table. If you add new crime data, be sure to
    recompute this table's values.

    """

    state = models.ForeignKey(State)
    year = models.IntegerField()
    number_of_cities = models.IntegerField()
    population = models.IntegerField(null=True)
    aggravated_assault = models.IntegerField(null=True)
    arson = models.IntegerField(null=True)
    burglary = models.IntegerField(null=True)
    forcible_rape = models.IntegerField(null=True)
    larceny_theft = models.IntegerField(null=True)
    motor_vehicle_theft = models.IntegerField(null=True)
    murder_and_nonnegligent_manslaughter = models.IntegerField(null=True)
    property_crime = models.IntegerField(null=True)
    robbery = models.IntegerField(null=True)
    violent_crime = models.IntegerField(null=True)

    aggravated_assault_rank_per100k = models.IntegerField()
    arson_rank_per100k = models.IntegerField()
    burglary_rank_per100k = models.IntegerField()
    forcible_rape_rank_per100k = models.IntegerField()
    larceny_theft_rank_per100k = models.IntegerField()
    motor_vehicle_theft_rank_per100k = models.IntegerField()
    murder_and_nonnegligent_manslaughter_rank_per100k = models.IntegerField()
    property_crime_rank_per100k = models.IntegerField()
    robbery_rank_per100k = models.IntegerField()
    violent_crime_rank_per100k = models.IntegerField()

    aggravated_assault_grade = models.CharField(null=True, max_length=1)
    arson_grade = models.CharField(null=True, max_length=1)
    burglary_grade = models.CharField(null=True, max_length=1)
    forcible_rape_grade = models.CharField(null=True, max_length=1)
    larceny_theft_grade = models.CharField(null=True, max_length=1)
    motor_vehicle_theft_grade = models.CharField(null=True, max_length=1)
    murder_and_nonnegligent_manslaughter_grade = models.CharField(null=True,
        max_length=1)
    property_crime_grade = models.CharField(null=True, max_length=1)
    robbery_grade = models.CharField(null=True, max_length=1)
    violent_crime_grade = models.CharField(null=True, max_length=1)

    class Meta:
        db_table = 'state_crime_stats'
        unique_together = (('state', 'year'),)

    def __unicode__(self):
        return '%s %s' % (self.year, self.state.name)

    def by_100k(self, field_name):
        """Get the requested field, but measured in per-100,000-population."""
        val = getattr(self, field_name)
        if val is None:
            return val
        return 1e5*val/max(1.0, self.population)


class CrimeContent(models.Model):
    population_type = models.CharField(max_length=10, choices=POPULATION_TYPES)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    content = models.TextField()

    def render(self, obj):
        content = self.content.replace('[TOWN]', obj.city_name).replace('[STATE]', obj.state)
        return content

    def __unicode__(self):
        return '%s - %s' % (self.population_type, self.grade)


class LocalAddress(models.Model):
    """
    Local address of all Protect America Locations.
    """
    street_name=models.CharField(max_length=255,blank=True,null=True)
    city=models.CharField(max_length=255,blank=True,null=True)
    state=models.CharField(max_length=255,blank=True,null=True)
    zip_code=models.IntegerField(max_length=5,blank=True,null=True)

    def __unicode__(self):
        return '%s, %s, %s, %s' % (self.street_name,self.city,self.state,self.zip_code)


class MatchAddressLocation(models.Model):
    """
    Match the local page of each city/state with an
    address of a local Protect America location
    """
    address=models.ForeignKey(LocalAddress)
    location=models.ForeignKey(CityLocation)

    def __unicode__(self):
        return '%s (%s)' % (self.address, self.location)

    def save(self, *args, **kwargs):
        addr_state=self.address.state
        match_state=self.location.state
        if addr_state != match_state:
            raise ValidationError('The states of the location and the address must match!')
        else:
            super(MatchAddressLocation,self).save(*args, **kwargs) 

class FeaturedCommon(models.Model):
    city = models.ForeignKey("CityLocation")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
class FeaturedVideo(FeaturedCommon):
    video_embed = models.CharField(max_length=255,blank=True,null=True)
    height = models.IntegerField(max_length=4,blank=False)
    width = models.IntegerField(max_length=4,blank=False)

    def __unicode__(self):
        return "%s's video " % self.city.city_name

class FeaturedIcon(FeaturedCommon):
    icon = models.ImageField(upload_to='featured_icons',height_field='image_height',width_field='image_width')
    image_height = models.CharField(max_length=255,blank=True,null=True,help_text='Auto populated height of image')
    image_width = models.CharField(max_length=255,blank=True,null=True,help_text='Auto populated width of image')

    def __unicode__(self):
        return "%s's icon" % self.city.city_name

class CityCompetitor(FeaturedCommon):
    rival = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s Competitor: %s" %(self.city.city_name,self.rival)




def return_sums(crime,state,city=None,year=2012,per100=False):
    if per100:
        if city:
            locations = CrimesByCity.objects.filter(year=year,fbi_city_name=city.title(),fbi_state=state.upper())
        else:
            locations = CrimesByCity.objects.filter(year=year,fbi_state=state.upper())
        end_string = '_rank_per100k'
        return CityCrimeStats.objects.filter(city=locations).aggregate(Sum(crime.lower()+end_string))
            
    else:
        if city:
            return CrimesByCity.objects.filter(year=year,fbi_city_name=city.title(),fbi_state=state.upper()).aggregate(Sum(crime.lower()))
        return CrimesByCity.objects.filter(year=year,fbi_state=state.upper()).aggregate(Sum(crime.lower()))
    

    
