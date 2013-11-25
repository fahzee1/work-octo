import csv
import json
from optparse import make_option
import re
from string import capwords

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Sum

from apps.crimedatamodels.models import (CrimesByCity, CityCrimeStats,
    State, StateCrimeStats)

class Command(BaseCommand):
    help = "Populate the database with volatile crime stats from the crimes_by_city table."
    option_list = BaseCommand.option_list + (
        make_option('--year', dest='year',
            help='Only recompute for a specific year'),)

    def handle(self, *args, **options):
        if options['year'] is not None:
            CityCrimeStats.objects.filter(year=options['year']).delete()
            compute_stats_for_year(options['year'])
            StateCrimeStats.objects.filter(year=options['year']).delete()
            compute_all_state_stats_for_year(options['year'])
        else:
            CityCrimeStats.objects.all().delete()
            compute_stats_for_all_years()
            StateCrimeStats.objects.all().delete()
            compute_all_state_stats_for_all_years()

def compute_stats_for_all_years():
    all_years = CrimesByCity.objects.values('year').distinct()
    all_years = [y['year'] for y in all_years]
    for year in all_years:
        compute_stats_for_year(year)

def compute_stats_for_year(year):
    crimes_for_all_cities = list(CrimesByCity.objects.filter(year=year))
    ranks_for_all_cities = initialize_ranked_crimes(crimes_for_all_cities)
    fields = filter(lambda f: f.endswith('_rank_per100k'),
        map(lambda f: f.name, CityCrimeStats._meta.local_fields))
    for field in fields:
        rank_on_crime_field(field, crimes_for_all_cities, ranks_for_all_cities)
        rylans_algorithm_a(field, crimes_for_all_cities, ranks_for_all_cities)
    save_ranks(ranks_for_all_cities)

def compute_all_state_stats_for_year(year):
    all_states = CrimesByCity.objects.values('fbi_state').distinct()
    all_states = [State.objects.get(abbreviation=s['fbi_state']) for s in
        all_states]
    all_states_stats = [initialize_state_stats(state, year) for state in
        all_states]
    compute_all_state_sums(all_states_stats)
    compute_all_state_ranks(all_states_stats)
    compute_all_state_grades(all_states_stats)
    save_state_stats(all_states_stats)
def compute_all_state_stats_for_all_years():
    all_years = CrimesByCity.objects.values('year').distinct()
    all_years = map(lambda y: y['year'], all_years)
    for year in all_years:
        compute_all_state_stats_for_year(year)

#@transaction.commit_manually
def save_state_stats(all_states_stats):
    for state_stats in all_states_stats:
        print "Saving %s %s" % (state_stats.state.name, state_stats.year)
        state_stats.save()
    transaction.commit()

def initialize_state_stats(state, year):
    cities_in_state = CrimesByCity.objects.filter(fbi_state=state.abbreviation,
        year=year)
    state_stats = StateCrimeStats(state=state, year=year)
    state_stats.cities = cities_in_state
    state_stats.number_of_cities = cities_in_state.count()
    return state_stats
def get_integer_fields():
    if hasattr(get_integer_fields, 'fields'): # cache in function attribute
        return get_integer_fields.fields      # just for fun
    fields = [c.name for c in CrimesByCity._meta.local_fields]
    [fields.remove(n) for n in ['id', 'fbi_state', 'fbi_city_name', 'year']]
    get_integer_fields.fields = fields
    return fields
def compute_all_state_sums(all_states_stats):
    for state_stats in all_states_stats:
        for field in get_integer_fields():
            sum = state_stats.cities.aggregate(sum=Sum(field)).get('sum', 0)
            setattr(state_stats, field, sum)
def compute_all_state_ranks(all_states_stats):
    for field in get_integer_fields():
        compute_all_state_ranks_for_field(all_states_stats, field)
def compute_all_state_ranks_for_field(all_states_stats, field):
    rank_bins = {}
    for state_stats in all_states_stats:
        by_100k = state_stats.by_100k(field)
        if by_100k is not None:
            by_100k = int(by_100k)
        if by_100k in rank_bins:
            rank_bins[by_100k].append(state_stats)
        else:
            rank_bins[by_100k] = [state_stats]
    rank_field = '%s_rank_per100k' % field
    for (index, (rank, states)) in enumerate(sorted(rank_bins.items())):
        for state_stats in states:
            setattr(state_stats, rank_field, index+1)
def compute_all_state_grades(all_states_stats):
    for field in get_integer_fields():
        rank_field = '%s_rank_per100k' % field
        grade_field = '%s_grade' % field
        grade_bins = {'A':[], 'B':[], 'C':[], 'D':[], 'F':[]}
        auto_graded = []
        rank_bins = {}
        for state_stats in all_states_stats:
            state_rank = getattr(state_stats, rank_field)
            if getattr(state_stats, field) is None:
                setattr(state_stats, grade_field, None)
                auto_graded.append(state_stats)
            elif state_rank in rank_bins:
                rank_bins[state_rank].append(state_stats)
            else:
                rank_bins[state_rank] = [state_stats]
        sorted_rank_bins = sorted(rank_bins.items())
        cities_remaining = len(all_states_stats) - len(auto_graded)
        for (bin_number, (grade, bin)) in enumerate(sorted(grade_bins.items())):
            bins_remaining = len(grade_bins.keys()) - bin_number
            bin_size = cities_remaining / bins_remaining
            while cities_remaining > 0:
                if len(grade_bins[grade]) > bin_size:
                    break
                (r, cities) = sorted_rank_bins.pop(0)
                grade_bins[grade].extend(cities)
                cities_remaining -= len(cities)
        for (grade, bin) in grade_bins.iteritems():
            for state_stats in bin:
                setattr(state_stats, grade_field, grade)

def initialize_ranked_crimes(crimes_for_all_cities):
    ranks_for_all_cities = {}
    for crimes_by_city in crimes_for_all_cities:
        ranks_for_all_cities[crimes_by_city] = CityCrimeStats(
            city=crimes_by_city, year=crimes_by_city.year)
    return ranks_for_all_cities
    
def rank_on_crime_field(rank_per100k_field, crimes_for_all_cities,
                        ranks_for_all_cities):
    per100k_field = re.sub(r'_rank', '', rank_per100k_field)
    crime_field = re.sub(r'_rank_per100k', '', rank_per100k_field)
    ranked_crimes_bins = {}
    for crime in crimes_for_all_cities:
        per100k_val = crime.by_100k(crime_field)
        bin_val = per100k_val
        if bin_val is not None:
            bin_val = int(per100k_val)
        if bin_val in ranked_crimes_bins:
            ranked_crimes_bins[bin_val].append(crime)
        else:
            ranked_crimes_bins[bin_val] = [crime]
    unique_crime_range = sorted(ranked_crimes_bins.keys())
    for (rank, bin_key) in enumerate(unique_crime_range):
        crimes_bin = ranked_crimes_bins[bin_key]
        for crime in crimes_bin:
            setattr(ranks_for_all_cities[crime], rank_per100k_field, rank+1)

def rylans_algorithm_a(rank_per100k_field, crimes_for_all_cities,
                       ranks_for_all_cities):
    """Grade that beautiful crime data.
    
    Attempt a uniform distribution of grades to cities based on rank.
    The 5 letter-grades form 5 buckets. The first bucket has size one-fifth
    the total number of cities. Once it's full, the second bucket has size
    one-fourth the number of remaining cities. Once the second bucket is full,
    the third bucket has size one-third the number of remaining cities, and
    so on until the cities are all slurped up and graded.

    """
    rank_bins = {}
    all_cities = ranks_for_all_cities.values()
    auto_graded = []
    for city in all_cities:
        rank = getattr(city, rank_per100k_field)
        crime_field = re.sub(r'_rank_per100k', '', rank_per100k_field)
        grade_field = re.sub(r'_rank_per100k', '_grade', rank_per100k_field)
        if getattr(city.city, crime_field) == 0: # give A grades to 0-crime
            setattr(city, grade_field, 'A')      # cities, but don't count
            auto_graded.append(city)             # them in the bucket
        elif getattr(city.city, crime_field) is None:
            setattr(city, grade_field, None)    # give None grades to
            auto_graded.append(city)            # None-crime cities
        elif rank in rank_bins:
            rank_bins[rank].append(city)
        else:
            rank_bins[rank] = [city]
    rank_list = sorted(rank_bins.items())
    grade_bins = {'A':[], 'B':[], 'C':[], 'D':[], 'F':[]}
    cities_remaining = len(all_cities) - len(auto_graded)
    for (bin_number, grade) in enumerate(sorted(grade_bins.keys())):
        bin_number = len(grade_bins.keys()) - bin_number
        bin_size = cities_remaining / bin_number
        while cities_remaining > 0:
            if len(grade_bins[grade]) > bin_size:
                break
            (r, cities) = rank_list.pop(0)
            grade_bins[grade].extend(cities)
            cities_remaining -= len(cities)
    grade_field = re.sub(r'_rank_per100k', '_grade', rank_per100k_field)
    for (grade, cities) in grade_bins.iteritems():
        for city in cities:
            setattr(city, grade_field, grade)

#@transaction.commit_manually
def save_ranks(ranks_for_all_cities):
    for rank in ranks_for_all_cities.values():
        print "Saving", rank.city.year, rank.city.fbi_city_name, \
            rank.city.fbi_state
        rank.save()
    transaction.commit()
