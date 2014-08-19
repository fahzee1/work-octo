import re
import pdb
import requests
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum,Q
from django.template.defaultfilters import slugify
from geopy import geocoders
from django.contrib.localflavor.us.models import (PhoneNumberField,
    USStateField)

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


RESOURCE_CHOICES = (
    ('rylan','Rylan'),
    ('waldy','Waldy'),
    ('cj','Cj')

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
    license = models.TextField(blank=True,null=True, help_text='License #')

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
    street_name = models.CharField(max_length=255,blank=True,null=True)
    city = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    phone_number = models.CharField(max_length=255,blank=True,null=True)
    zip_code = models.IntegerField(max_length=5,blank=True,null=True)
    googleplus_url = models.CharField(max_length=255,blank=True,null=True)

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
    video_embed = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return "%s's video " % self.city.city_name

class FeaturedIcon(FeaturedCommon):
    icon = models.ImageField(upload_to='featured_icons',height_field='image_height',width_field='image_width')
    image_height = models.CharField(max_length=255,blank=True,null=True,help_text='Auto populated height of image')
    image_width = models.CharField(max_length=255,blank=True,null=True,help_text='Auto populated width of image')

    def __unicode__(self):
        return "%s's icon" % self.city.city_name

class CityCompetitor(FeaturedCommon):
    rival = models.CharField(max_length=255,help_text='Name of our competitor?')
    door_window = models.CharField(default='3',max_length=255,help_text='Door/Window protection?')
    alarm_monitoring = models.BooleanField(default=False,help_text='24/7 Alarm Monitoring?')
    free_equipment = models.BooleanField(default=False,help_text='Free security equipment?')
    no_fees = models.BooleanField(default=False,help_text='No installation fees')
    warranty = models.BooleanField(default=False,help_text='Lifetime equipment warrant?')
    monthly_cost = models.CharField(default='19.99',max_length=255,help_text='How much a month?')


    def __unicode__(self):
        return "%s Competitor: %s" %(self.city.city_name,self.rival)




class Resources(models.Model):
    """
    used to show resources section on local pages
    """

    city = models.ForeignKey("CityLocation",blank=True,null=True)
    state = models.ForeignKey("State")
    name = models.CharField(max_length=255)
    url = models.TextField()
    category = models.CharField(max_length=200,choices=RESOURCE_CHOICES)

    def __unicode__(self):
        return '%s - %s' % (self.name,self.city)


class CityAndState(models.Model):
    city = models.CharField(max_length=24)
    state = USStateField(max_length=24)
    zip = models.CharField(max_length=5, unique=True,blank=True,null=True)

    class Meta:
        abstract = True





PROPERTY_CHOICES = (
        ('r','residential'),
        ('c','commerical'),

    )
class Permits(CityAndState):
    permit_fee = models.CharField(max_length=255,blank=True,null=True)
    permit_url = models.CharField(max_length=255,blank=True,null=True)
    addendum_fee = models.CharField(max_length=255,blank=True,null=True)
    addendum_template = models.CharField(max_length=255,blank=True,null=True)
    property_type = models.CharField(max_length=255,blank=True,null=True, choices=PROPERTY_CHOICES)
    no_tech_install = models.BooleanField(default=True)
    no_self_install = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s, %s permits' % (self.city,self.state)



class Demographics(CityAndState):
    """
    affordability_avgHomeValue, home_ownVsRent,home_homeSize
    are charts.

    home_ownVsRent is depreciated

    Data pulled from Zillows API for local pages
    """
    avg_commute_time = models.CharField(max_length=255,blank=True,null=True)
    median_age = models.CharField(max_length=255,blank=True,null=True)
    median_household_income = models.CharField(max_length=255,blank=True,null=True)
    median_home_size = models.CharField(max_length=255,blank=True,null=True)
    median_list_price = models.CharField(max_length=255,blank=True,null=True)
    owners_renters = models.CharField(max_length=255,blank=True,null=True,help_text='Percent of home owners to renters')
    median_list_price = models.CharField(max_length=255,blank=True,null=True)
    chart_avgHomeValue = models.CharField(max_length=255,blank=True,null=True)
    chart_homeSize = models.CharField(max_length=255,blank=True,null=True)
    chart_ownVsRent = models.CharField(max_length=255,blank=True,null=True)

    def __unicode__(self):
        return '%s, %s Demographics' % (self.city,self.state)


    @classmethod
    def call_zillow(cls,city,state):
        from bs4 import BeautifulSoup
        try:
            r = requests.get('http://www.zillow.com/webservice/GetDemographics.htm?zws-id=%s&state=%s&city=%s' % (settings.ZILLOW,state,city), timeout=10)
            if r.status_code == 200:
                data = {}
                soup = BeautifulSoup(r.text)
                code = int(soup.message.code.contents[0])
                if code == 0:
                    # success
                    # get charts
                    for chart in soup.find_all('chart'):
                        chart_url = None
                        if chart.find('name').contents[0] == 'Median Home Value':
                            chart_url = chart.find('url').contents[0]
                            data['avgHomeValue'] = chart_url

                        if chart.find('name').contents[0] == 'Home Size in Square Feet':
                            chart_url = chart.find('url').contents[0]
                            data['homeSize'] = chart_url

                        if chart.find('name').contents[0] == 'Owners vs. Renters':
                            chart_url = chart.find('url').contents[0]
                            data['ownVsRent'] = chart_url










            else:
                return None

        except requests.exceptions.Timeout:
            print 'timed out'
            return None




class Universities(CityAndState):
    """
    Data pulled from inventory.data.gov
    """
    instnm = models.CharField(max_length=255,blank=True,null=True, help_text='University Name')
    website = models.CharField(max_length=255,blank=True,null=True, help_text='Website')
    addr = models.CharField(max_length=255,blank=True,null=True, help_text='Address')

    def __unicode__(self):
        return '%s, %s Universities' % (self.city,self.state)


class LocalEducation(CityAndState):
    """
    Data pulled from inventory.data.gov
    """

    name = models.CharField(max_length=255,blank=True,null=True, help_text='Local education name')

    def __unicode__(self):
        return '%s, %s Local Education' % (self.city,self.state)


class FarmersMarket(CityAndState):
    """
    Data pulled from search.ams.usda.gov
    """
    name = models.CharField(max_length=255,blank=True,null=True, help_text='Market name')
    website = models.CharField(max_length=255,blank=True,null=True, help_text='Website')

    def __unicode__(self):
        return '%s, %s FarmersMarket' % (self.city,self.state)










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



