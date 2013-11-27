# Common Django settings for web project.
import sys
import os
import settings
import logging
import logging.handlers


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(settings.PROJECT_ROOT, 'src', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(settings.PROJECT_ROOT, 'src', 'static')

STATIC_URL = '/static/'

STASTICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*$#jqy%8ho+3-n9adsj@qjgq8-+h6oz8z3&2k5g5&9mzhx#tj('

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.core.context_processors.request",
    'django.core.context_processors.debug',
    'apps.common.context_processors.business_hours',
    'apps.common.context_processors.phone_number',
    'apps.common.context_processors.mobile_check',
    'apps.common.context_processors.tracking_pixels',
    'apps.pricetable.context_processors.price_table',
    'apps.pricetable.context_processors.current_cart',
    'apps.adspace.context_processors.campaign',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
    'apps.common.context_processors.last_day_of_month',
    'apps.common.context_processors.business_time',
    'apps.common.context_processors.detect_agent_id',
    'django.contrib.messages.context_processors.messages',
    )


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    # 'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'apps.affiliates.middleware.AffiliateMiddleware',
    'apps.common.middleware.SearchEngineReferrerMiddleware',
    'apps.common.middleware.CommonMiddlewareWrapper',
    'apps.common.middleware.DetectMobileBrowser',
    'apps.common.middleware.LocalPageRedirect',
    'django.middleware.cache.FetchFromCacheMiddleware',
    #'apps.newsfeed.middleware.RenderNewsFeed',
    #'apps.newsfeed.middleware.GetGeoIp',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(settings.PROJECT_ROOT, 'src', 'templates'),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.comments',

    'south',
    'sekizai',
    'colorful',

    'apps.common',
    'apps.affiliates',
    'apps.sitemaps',
    'apps.adspace',
    'apps.contact',
    'apps.pricetable',
    'apps.search',
    'apps.testimonials',
    'apps.crimedatamodels',
    'apps.news',
    'apps.crm',
    'apps.payitforward',
    'apps.emails',
    'apps.faqs',
    'apps.events',
    'apps.newsfeed',

    # sitemaps by opm
    'apps.pa-sitemaps',
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

DEFAULT_PHONE = '8009515190'
SUPER_AFFILIATES = ("a10058","a10447","a10449")


GEOIP_PATH = os.path.join(settings.PROJECT_ROOT, 'src', 'apps', 'crimedatamodels', 'external', 'data')

INTERNAL_IPS = ('127.0.0.1')


TWITTER_CONSUMER_KEY = 'neNxtJ7k9R0UKTfwx12OnA'
TWITTER_CONSUMER_SECRET = 'gAN1yKQXv6Z8JXKoJngKKd382nxzw2VrTdgHu0LBjU'
TWITTER_ACCESS_TOKEN = '199333362-iUqm5j0TqbufpKcQRlPyuOqiwMArfLzwl0nmY3CJ'
TWITTER_ACCESS_TOKEN_SECRET = 'jWBAmeUpFTZbpfyX7kXKhSJVWqow3uhtV8fRfI39URA'
SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = True


READY_FOR_STATIC = False

#keyword list for local pages
LOCAL_KEYWORDS = ['home-security-systems-reviews', 'best-home-security-systems', 'home-security-systems-comparison', 'diy-home-security-systems', 'home-security-systems-consumer-reports', 'ge-home-security-systems', 'home-security-system', 'best-home-security-system', 'honeywell-home-security-systems', 'compare-home-security-systems', 'home-security-system-reviews', 'monitronics-home-security-systems', 'top-home-security-systems', 'home-security-systems-review', 'home-security-camera-systems', 'home-security-systems-ratings', 'home-security-systems-rating', 'wireless-home-security-system-reviews', 'ge-home-security-system', 'diy-home-security-system', 'wireless-home-security-systems-reviews', 'home-security-store-home-security-systems', 'in-home-security-systems', 'free-home-security-systems', 'wired-home-security-system', 'monitored-home-security-systems', 'self-install-home-security-systems', 'home-security-systems-companies', 'home-security-system-monitoring', 'home-security-alarm-systems', 'cheap-home-security-system', 'home-security-systems-cost', 'home-surveillance-systems', 'home-security-systems-reviews', 'best-home-security-systems', 'home-security-systems-comparison', 'diy-home-security-systems', 'home-security-systems-consumer-reports', 'ge-home-security-systems', 'home-security-system', 'best-home-security-system', 'compare-home-security-systems', 'home-security-system-reviews', 'monitronics-home-security-systems', 'top-home-security-systems', 'home-security-systems-review', 'home-security-camera-systems', 'home-security-systems-ratings', 'home-security-systems-rating', 'ge-home-security-system', 'diy-home-security-system', 'home-security-store-home-security-systems', 'in-home-security-systems', 'free-home-security-systems', 'wired-home-security-system', 'monitored-home-security-systems', 'self-install-home-security-systems', 'home-security-systems-companies', 'home-security-system-monitoring', 'home-security-alarm-systems', 'cheap-home-security-system', 'home-security-systems-cost', 'home-surveillance-systems', 'home-surveillance-system', 'wireless-home-surveillance-systems', 'best-home-surveillance-system', 'home-video-surveillance-systems', 'home-surveillance-systems-reviews', 'home-surveillance-system-reviews', 'outdoor-home-surveillance-systems', 'home-video-surveillance-system', 'home-security-surveillance-systems', 'home-surveillance-cameras', 'hidden-home-surveillance-systems', 'surveillance-systems', 'wireless-surveillance-system', 'video-surveillance-systems', 'home-surveillance', 'best-home-surveillance-systems', 'home-video-surveillance', 'home-surveillance-camera', 'video-surveillance-system', 'surveillance-camera-system', 'surveillance-system', 'surveillance-camera-systems', 'wireless-surveillance-systems', 'security-surveillance-systems', 'home-surveillance-camera-systems', 'home-surveillance-equipment', 'home-surveillance-systems-review', 'camera-surveillance-systems', 'wireless-home-surveillance-system', 'best-home-surveillance-system-reviews', 'home-security-surveillance', 'home-video-surveillance-systems-reviews', 'diy-home-surveillance-systems', 'wireless-home-video-surveillance-systems', 'surveillance-systems-reviews', 'wireless-surveillance-camera-system', 'surveillance-system-reviews', 'dvr-surveillance-system', 'home-surveillance-camera-system', 'home-security-surveillance-system', 'cheap-home-surveillance-systems', 'home-camera-surveillance', 'wireless-video-surveillance-systems', 'surveillance-cameras-systems', 'home-surveillance-systems-iphone', 'camera-surveillance-system', 'outdoor-surveillance-systems', 'adt-pulse','adt-pulse-cost','adt-pulse-pricing','adt-pulse-pricing','adt-pulse-security','adt-security-pulse','adt-pulse-price','pulse-adt','adt-pulse-system','adt-home-alarm','adt-home-alarms','adt-security-services','wireless-home-security-systems', 'wireless-home-security-products', 'wireless-home-security', 'home-surveillance-systems-wireless','wireless-home-security-systems-reviews', 'wireless-home-security-system-reviews', 'home-security-systems-wireless','wireless-home-security-system', 'wireless-home-security-systems', 'home-security-systems-wireless', 'wireless-home-security-system','wireless-home-security-systems','wireless-alarm-systems','wireless-alarms', 'wireless-alarm-system','best-wireless-alarm-system','top-wireless-security-systems','best-wireless-homesecurity-systems','wireless-homesecurity','wireless-ge-security',]
CUSTOM_KEYWORD_LIST = ['']
WIRELESS_KEYWORD_LIST = ['wireless-home-security-systems', 'wireless-home-security-products', 'wireless-home-security', 'home-surveillance-systems-wireless','wireless-home-security-systems-reviews', 'wireless-home-security-system-reviews', 'home-security-systems-wireless','wireless-home-security-system', 'wireless-home-security-systems', 'home-security-systems-wireless', 'wireless-home-security-system','wireless-home-security-systems','wireless-alarm-systems','wireless-alarms', 'wireless-alarm-system','best-wireless-alarm-system','top-wireless-security-systems','best-wireless-homesecurity-systems','wireless-homesecurity','wireless-ge-security','wireless-ge-security']
ADT_KEYWORD_LIST = ['adt-pulse','adt-pulse-cost','adt-pulse-pricing','adt-pulse-pricing','adt-pulse-security','adt-security-pulse','adt-pulse-price','pulse-adt','adt-pulse-system','adt-home-alarm','adt-home-alarms','adt-security-services']
#path where all the local page files reside. Using file backed system instead of DB backed
LOCAL_PAGE_PATH = '/virtual/customer/www2.protectamerica.com/localpages/'

#exclude these cities for local pages and create respective static pages
EXCLUDE_CITIES = {
'New York':'NY',
'Los Angeles':'CA',
'Chicago':'IL',
'Washington':'DC',
'Boston':'MA',
'San Jose':'CA',
'Philadelphia':'PA',
'Dallas':'TX',
'Houston':'TX',
'Atlanta':'GA',
'Miami':'FL',
'Detroit':'MI',
'Phoenix':'AZ',
'Seattle':'WA',
'Minneapolis':'MN'
}

TIMEZONES = {
    'AL': 'America/Chicago',
    'AK': 'America/Anchorage',
    'AZ': 'America/Phoenix',
    'AR': 'America/Chicago',
    'CA': 'America/Los_Angeles',
    'CO': 'America/Denver',
    'CT': 'America/New_York',
    'DE': 'America/New_York',
    'DC': 'America/New_York',
    'FL': 'America/New_York',
    'GA': 'America/New_York',
    'HI': 'Pacific/Honolulu',
    'ID': 'America/Denver',
    'IL': 'America/Chicago',
    'IN': 'America/Indianapolis',
    'IA': 'America/Chicago',
    'KS': 'America/Chicago',
    'KY': 'America/New_York',
    'LA': 'America/Chicago',
    'ME': 'America/New_York',
    'MD': 'America/New_York',
    'MA': 'America/New_York',
    'MI': 'America/New_York',
    'MN': 'America/Chicago',
    'MS': 'America/Chicago',
    'MO': 'America/Chicago',
    'MT': 'America/Denver',
    'NE': 'America/Chicago',
    'NV': 'America/Los_Angeles',
    'NH': 'America/New_York',
    'NJ': 'America/New_York',
    'NM': 'America/Denver',
    'NY': 'America/New_York',
    'NC': 'America/New_York',
    'ND': 'America/Chicago',
    'OH': 'America/New_York',
    'OK': 'America/Chicago',
    'OR': 'America/Los_Angeles',
    'PA': 'America/New_York',
    'RI': 'America/New_York',
    'SC': 'America/New_York',
    'SD': 'America/Chicago',
    'TN': 'America/Chicago',
    'TX': 'America/Chicago',
    'UT': 'America/Denver',
    'VT': 'America/New_York',
    'VA': 'America/New_York',
    'WA': 'America/Los_Angeles',
    'WV': 'America/New_York',
    'WI': 'America/Chicago',
    'WY': 'America/Denver'
}


WEATHER_CODE_MAP = {
    '395': 'snow',
    '392': 'snow',
    '389': 'rain',
    '386': 'rain',
    '377': 'snow',
    '374': 'snow',
    '371': 'snow',
    '368': 'rain',
    '365': 'rain',
    '362': 'snow',
    '359': 'rain',
    '356': 'rain',
    '353': 'rain',
    '350': 'snow',
    '338': 'snow',
    '335': 'snow',
    '332': 'snow',
    '329': 'snow',
    '326': 'snow',
    '323': 'snow',
    '320': 'rain',
    '317': 'rain',
    '314': 'rain',
    '311': 'rain',
    '308': 'rain',
    '305': 'rain',
    '302': 'rain',
    '299': 'rain',
    '296': 'rain',
    '293': 'rain',
    '284': 'rain',
    '281': 'rain',
    '266': 'rain',
    '263': 'rain',
    '260': 'smoke',
    '248': 'smoke',
    '230': 'snow',
    '227': 'snow',
    '200': 'lightning',
    '185': 'rain',
    '182': 'rain',
    '179': 'rain',
    '176': 'rain',
    '143': 'smoke',
    '122': 'partly-cloudy',
    '119': 'cloudy',
    '116': 'partly-cloudy',
    '113': 'sunny',
}

#LeadConduit data
LEAD_ACCOUNT_ID = '1626fa3'
LEAD_CAMPAIGN_ID = '054irukv1'
# this variable is used in lead forms and black friday forms
# use it so while testing we disable emails
LEAD_TESTING = False



# override these settings with those from settings.local,
# which may be a symlink to your local, version-controlled settings
try:
    from etc.django.local import *
except ImportError:
    pass
#Silverpop Engage credentials for unsubscribe.htm

ENGAGE_CONFIG = {
    'username': 'kevin@protectamerica.com',
    'password': '8RYbZ&YX',
    'api_url': 'http://api3.silverpop.com/XMLAPI',
    'ftp_url': 'transfer3.silverpop.com',
}

# Siverpop Engage Master Suppression List ID
ENGAGE_UNSUBSCRIBE_MSL_ID = '1788700'

# Silverpop Engage logging for unsubscribe.htm
ENGAGE_LOG_DIR = '/virtual/customer/www2.protectamerica.com/logs/silverpop_unsubscribe.log'
ENGAGE_LOG_LEVEL = logging.INFO
ENGAGE_LOG_ROTATION = {
    'maxBytes': 1048576,  # 1MB
    'backupCount': 5
}

# depending on where/what user is running this code LC_LOG (lead conduit log) will be
# one of the values below. It will either be a local directory or the directory on 
# the live server 


# override these settings with those from settings.local,
# which may be a symlink to your local, version-controlled settings
try:
    from etc.django.local import *
except ImportError:
    pass

# one of the values below. It will either be a local directory or the directory on
# the live server
if os.path.isdir('/Users/cjogbuehi'):
    LC_LOG = ('/Users/cjogbuehi/virtualenvs/example.log' if LEAD_TESTING else '/virtual/customer/www2.protectamerica.com/logs/leadconduit.log')
elif os.path.isdir('/Users/rylanfrancis'):
    LC_LOG = ('/Users/rylanfrancis/example.log' if LEAD_TESTING else '/virtual/customer/www2.protectamerica.com/logs/leadconduit.log')
elif os.path.isdir('/Users/edgarrodriguez'):
    LC_LOG = ('/Users/edgarrodriguez/logs/example.log' if LEAD_TESTING else '/virtual/customer/www2.protectamerica.com/logs/leadconduit.log')
else:
    LC_LOG = '/virtual/customer/www2.protectamerica.com/logs/leadconduit.log'

# Build logging for unsubscribe.htm
sp_logger = logging.getLogger('silverpoppy.api')
sp_logger.setLevel(ENGAGE_LOG_LEVEL)
handler = logging.handlers.RotatingFileHandler(ENGAGE_LOG_DIR,
                                            **ENGAGE_LOG_ROTATION)
handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s - %(message)s'))
sp_logger.addHandler(handler)

