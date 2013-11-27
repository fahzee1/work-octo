import os
import settings
# Local Django settings for web project.
ADMIN_REMOVE_DEBUG=True
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ['VIRTUAL_ENV'] + '/local/protectamerica.db',
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SITE_ID=0


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

if not ADMIN_REMOVE_DEBUG:
    from etc.django.common import MIDDLEWARE_CLASSES,INSTALLED_APPS
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False,}


LC_LOG = os.environ['VIRTUAL_ENV'] + '/local/leadconduit.log'
ENGAGE_LOG_DIR = os.environ['VIRTUAL_ENV'] + '/local/silverpop_unsubscribe.log'
