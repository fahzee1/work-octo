"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from models import (LocalAddress, MatchAddressLocation,
	                ZipCode, State, CityLocation, CrimesByCity)
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

	def test_to_make_sure_tests_work(self):
		addr=LocalAddress.objects.create(street_name="123 paper st",
										 city="Austin",
										 state="TX",
										 zip_code=77777)
		_all=LocalAddress.objects.all().count()
		self.assertEqual(_all,1)
		self.assertEqual(addr.zip_code,77777)


	def test_match_doesnt_save(self):
		'''
			addr=123 paper st, Austin, TX
			error_var=Hayward,CA
			MatchAddressLocation doesnt save/create when the states
			arent the same so I'm testing for an error 
		'''
		addr=LocalAddress.objects.get(street_name="123 paper st")
		error_var=CityLocation.objects.get(pk=580)
		try:
			thetest=MatchAddressLocation.objects.create(address=addr,location=error_var)
			if thetest:
				self.assertEqual(thetest.address.street_name,"123 paper st")
		except ValidationError:
			#this is what I wanted
			return True 
		


