from django.core.urlresolvers import reverse
from django.db import models


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
    abbreviation = models.CharField(max_length=2, unique=True)

    def __unicode__(self):
        return '%s %s' % (self.abbreviation, self.name)

    class Meta:
        db_table = 'states'

    def get_absolute_url(self):
        return reverse('crime-rate:choose-city', args=[self.abbreviation])


class CityLocation(models.Model):
    city_name = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,
        db_index=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,
        db_index=True)

    class Meta:
        db_table = 'citylocations'
        unique_together = (('city_name', 'state'),)

    def get_absolute_url(self):
        return reverse('crime-rate:crime-stats', args=[self.state,
            self.city_name])

    def __unicode__(self):
        return '%s, %s' % (self.city_name, self.state)


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

    class Meta:
        db_table = 'city_crime_stats'
        unique_together = (('city', 'year'),)


class StateCrimeStats(models.Model):
    """Volatile state crime stats computed from the CrimesByCity table.

    These stats are volatile--changing any data in CrimesByCity invalidates
    the correctness of this table. If you add new crime data, be sure to
    recompute this table's values.

    """
    
    state = models.ForeignKey(State)
    year = models.IntegerField()
    number_of_cities = models.IntegerField()
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
