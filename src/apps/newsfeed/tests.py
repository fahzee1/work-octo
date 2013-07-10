"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import date, timedelta
from django.test import TestCase,TransactionTestCase
from models import TheFeed,AddType,FallBacks
from middleware import GetGeoIp
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from mock import Mock 
import requests





class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class AddTypeTest(TestCase):

	def setUp(self):
		self.one_word=AddType.objects.create(name='spirits')
		self.two_word=AddType.objects.create(name='spirit drinks')
		#self.three_word=AddType.objects.create(name='Spirit Drinks Things')


	def test_type_is_two_words(self):
		'''
		test that type is only one or two words 
		anymore will throw error
		'''

		self.assertTrue(self.one_word)
		self.assertEqual(self.one_word.name,'Spirits')
		self.assertTrue(self.two_word)
		self.assertEqual(self.two_word.name,'Spirit Drinks')
		#self.assertFalse(three_word)
		#self.assertRaisesMessage(ValidationError,'Name should be two words only',three_word)



class TheFeedTest(TestCase):
	fixtures=['newsfeed.json']

	def setUp(self):
		self.expire=date.today()+timedelta(days=2)
		self.thetype=AddType.objects.get(name="Date Based")
		self.drake=TheFeed.objects.get(name="Drake")
		self.new_feed=TheFeed.objects.create(name='New Feed',
			                            city='austin',
			                            state='TX',
			                            message='News feed test',
			                            expires=self.expire,
			                            type=self.thetype)


	def test_works(self):
		self.assertTrue(self.drake)
		self.assertTrue(self.new_feed)

	def test_TheFeed_methods(self):
		locale=self.new_feed.location()
		not_expired=self.new_feed.feed_expired()
		is_expired=self.drake.feed_expired()
		self.assertEqual(locale,'Austin,TX')
		self.assertFalse(not_expired)
		self.assertTrue(is_expired)

'''
class TheFeedMiddlewareTest(TestCase):
	fixtures=['newsfeed.json']

	def setUp(self):
		self.rnf=GetGeoIp()
		self.request=Mock()
		self.request.session={}
		self.request.GET={'city':'Austin','state':'TX'}
		self.request.META={'REMOTE_ADDR':'127.0.0.1:8000'}

	
	def test_process_request_empty(self):
		self.assertEqual(self.request.session,{})
		self.assertEqual(self.rnf.process_request(self.request),None)

	def test_process_request_full(self):
		make_request=self.rnf.process_request(self.request)
		self.assertTrue(self.request.session)
		self.assertTrue(self.request.backup)

	def test_http_response(self):
		self.request.session['GeoFeedData']={'geodate':'1/2/3'}
		make_request=self.rnf.process_request(self.request)
		self.assertEqual(make_request.status_code,200)

	def test_sets_session(self):
		make_request=self.rnf.process_request(self.request)
		self.assertTrue(self.request.session)
		self.assertTrue(self.request.session['GeoFeedData'])

'''





