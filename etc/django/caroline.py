import os
import settings
# Local Django settings for web project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID=1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/Users/caroline/Sites/protectamerica/database.db',                      # Or path to database file if using sqlite3
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# EMAIL information
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BUSINESS_HOURS = [{
    #monday
    'start': '0700',
    'end': '2300',
},{
    #tuesday
    'start': '0700',
    'end': '2300',
},{
    #wednesday
    'start': '0700',
    'end': '2300',
},{
    #thursday
    'start': '0700',
    'end': '2300',
},{
    #friday
    'start': '0700',
    'end': '2300',
},{
    #saturday
    'start': '0800',
    'end': '2000',
},{
    #sunday
    'start': '0900',
    'end': '2100',
}]

WEBSITE_TEMPLATE = 'patwo'
TEMPLATE_DIRS = (
    os.path.join(settings.PROJECT_ROOT, 'src', 'templates'),
    os.path.join(settings.PROJECT_ROOT, 'src', 'templates', WEBSITE_TEMPLATE),

)
STATICFILES_DIRS = (
    os.path.join(TEMPLATE_DIRS[1], 'static'),
)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

GEOIP_LIBRARY_PATH = '/usr/local/lib/libGeoIP.so'

LC_LOG = '/Users/caroline/leadconduit.log'
ENGAGE_LOG_DIR = '/Users/caroline/silverpop_unsubscribe.log'