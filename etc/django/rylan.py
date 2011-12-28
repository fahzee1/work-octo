import os
import settings
# Local Django settings for web project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/Users/rylanfrancis/Documents/protectamerica2/protectamerica.dev/database.db',                      # Or path to database file if using sqlite3
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# EMAIL information
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BUSINESS_HOURS = [{   
    #monday
    'start': '0800',
    'end': '2100',
},{
    #tuesday
    'start': '0800',
    'end': '2100',
},{
    #wednesday
    'start': '0800',
    'end': '2100',
},{
    #thursday
    'start': '0800',
    'end': '2100',
},{
    #friday
    'start': '0800',
    'end': '2100',
},{
    #saturday
    'start': '0800',
    'end': '1700',
},]

WEBSITE_TEMPLATE = 'patwo'
TEMPLATE_DIRS = (
    os.path.join(settings.PROJECT_ROOT, 'src', 'templates'),
    os.path.join(settings.PROJECT_ROOT, 'src', 'templates', WEBSITE_TEMPLATE),

)
STATICFILES_DIRS = (
    os.path.join(TEMPLATE_DIRS[1], 'static'),
)
