"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from models import (LocalAddress, MatchAddressLocation,
	                ZipCode, State, CityLocation, CrimesByCity)
from django.core.exceptions import ValidationError
from apps.crimedatamodels.views import query_by_state_city
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}


class Test_Local_Address_And_Match(TestCase):
	fixtures=['crime_data_and_locations']

	def setUp(self):
		from django.conf import settings
		settings.SITE_ID=4
		self.addr=LocalAddress.objects.get(street_name="123 paper st")  

	def test_to_make_sure_tests_work(self):
		addr=LocalAddress.objects.create(street_name="123 paper st",
										 city="Austin",
										 state="TX",
										 zip_code=77777)
		_all=LocalAddress.objects.filter(zip_code=77777).count()
		self.assertEqual(_all,1)
		self.assertEqual(addr.street_name,"123 paper st")


	def test_match_doesnt_save(self):
		'''
			addr = 123 paper st, Austin, TX
			error_var = Hayward,CA
			MatchAddressLocation doesnt save/create when the states
			arent the same so testing for an error 
		'''

		error_var=CityLocation.objects.get(pk=580)
		try:
			thetest=MatchAddressLocation.objects.create(address=self.addr,location=error_var)
			if thetest:
				self.assertEqual(thetest.address.street_name,"123 paper st")
		except ValidationError:
			#this is what I wanted
			return True 

	def test_match_does_save(self):
		'''
			addr = 123 paper st, Austin, TX
			right_var = Abernathy, Tx
			Should have successful save because the states
			match
		'''
		correct_var=CityLocation.objects.get(pk=6434)
		try:
			thetest=MatchAddressLocation.objects.create(address=self.addr,location=correct_var)
			self.assertTrue(thetest)
		except ValidationError:
			#this is not what i want
			return False


class Test_Crime_Data_Models(TestCase):
	fixtures=['crime_data_and_locations']

	def setUp(self):
		from django.conf import settings
		settings.SITE_ID=4
		self.addr=LocalAddress.objects.get(street_name="123 paper st") 
		self.locale=CityLocation.objects.get(pk=6434)
		self.matched_locale=MatchAddressLocation.objects.create(address=self.addr,location=self.locale)

	def test_query_state_city(self):
		city="Austin"
		state="TX"
		_city="Abernathy"
		thetest=query_by_state_city(state,city)
		_thetest=query_by_state_city(state,_city)

		#regular context i should receive without a location match
		ctx=[ thetest["crime_stats"],
		      thetest["years"],
		      thetest["latest_year"],
		      thetest["state"],
		      thetest["state_long"],
		      thetest["city"],
		      thetest["lat"],
		      thetest["long"],
		      thetest["weather_info"],
		      thetest["pop_type"],
		      thetest["city_id"],
		      thetest["content"] 
		     ]
		#additonal context ill recieve if there was a location match
		matched_ctx=[ _thetest["local_street"],
			   _thetest["local_state"],
			   _thetest["local_city"],
			   _thetest["local_zipcode"]
			]      
		
		self.assertTrue(thetest)
		self.assertTrue(ctx)
		self.assertTrue(_thetest)
		self.assertTrue(matched_ctx)

	def test_local_state_and_city(self):
		local_state=self.client.get(reverse("local-state"))
		local_city=self.client.get(reverse("choose-city",kwargs={"state":"TX"}))
		local_page=self.client.get(reverse("local-page",kwargs={"state":"TX", "city":"Austin"}))
		print 'local state is %s' % local_state

		try:
			local_page.context["local_street"]
			local_page.context["local_state"],
			local_page.context["local_city"],
			local_page.context["local_zipcode"]
		except TypeError:
			local_street_ctx=None
			local_state_ctx=None
			local_city_ctx=None
			local_zipcode_ctx=None
			

		self.assertEqual(local_state.status_code,200)
		self.assertEqual(local_city.status_code,200)
		self.assertEqual(local_page.status_code,301)
		self.assertIsNone(local_street_ctx)
		self.assertIsNone(local_state_ctx)
		self.assertIsNone(local_city_ctx)
		self.assertIsNone(local_zipcode_ctx)
		self.assertIn("basic",local_city.context["forms"])
		self.assertIn("basic",local_state.context["forms"])



class TestFreeCrimeStats(TestCase):
	fixtures=['crime_data_and_locations']

	def setUp(self):
		from django.conf import settings
		settings.SITE_ID=23

	def test_search(self):
		search=self.client.get("search",{'q':'Austin'})
		self.assertEqual(search.status_code,200)
		self.assertIn('num_cities',search.context)
		self.assertIn('cities',search.context)
		











		


