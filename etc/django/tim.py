import os
import settings
# Local Django settings for web project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/tim/batcave/misc/pasite/database.db',
    }
}

# EMAIL information
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BUSINESS_HOURS = [
    {'start': '0700', 'end': '2300'},
    {'start': '0700', 'end': '2300'},
    {'start': '0700', 'end': '2300'},
    {'start': '0700', 'end': '2300'},
    {'start': '0700', 'end': '2300'},
    {'start': '0800', 'end': '2000'},
    {'start': '0900', 'end': '2100'},
]

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
