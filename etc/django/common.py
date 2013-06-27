# Common Django settings for web project.
import sys
import os
import settings


DEBUG = True
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
    'django.middleware.cache.FetchFromCacheMiddleware',
    'apps.newsfeed.middleware.RenderNewsFeed',
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
SUPER_AFFILIATES = ("a10058",)


GEOIP_PATH = os.path.join(settings.PROJECT_ROOT, 'src', 'apps', 'crimedatamodels', 'external', 'data')

INTERNAL_IPS = ('127.0.0.1')


TWITTER_CONSUMER_KEY='neNxtJ7k9R0UKTfwx12OnA'
TWITTER_CONSUMER_SECRET='gAN1yKQXv6Z8JXKoJngKKd382nxzw2VrTdgHu0LBjU'
TWITTER_ACCESS_TOKEN='199333362-iUqm5j0TqbufpKcQRlPyuOqiwMArfLzwl0nmY3CJ'
TWITTER_ACCESS_TOKEN_SECRET='jWBAmeUpFTZbpfyX7kXKhSJVWqow3uhtV8fRfI39URA'

# override these settings with those from settings.local,
# which may be a symlink to your local, version-controlled settings
try:
    from etc.django.local import *
except ImportError:
    pass
