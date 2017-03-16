#############################################################################
# Django settings for PortfolioRiskManagement Project.

import os
from os.path import abspath, basename, dirname, join, normpath
import django


DJANGO_VERSION = 100*django.VERSION[0] + 10*django.VERSION[1]+ django.VERSION[2]
print("DJANGO_VERSION ",str(django.VERSION[0])+'.' + str(django.VERSION[1])+'.' + str(django.VERSION[2]))

BASE_DIR = os.getcwd() 
print("BASE DIRECTORY: ",BASE_DIR)

###############################################################################
## General
DEBUG=True
ALLOWED_HOSTS = [
  '*'
]
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
SECRET_KEY = '8@-3463gga46uasg+cm^7x05y*14gfgadrgw4634@ic$agaasdgggujs^'
ROOT_URLCONF = 'urls'  



LOGIN_REDIRECT_URL = '/'


###############################################################################
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'app.models',
    'app.modules',

    'app',
    'rest_framework',

    'app.management',
    'app.dataManage',
    'app.fields',

    'app.reporting_modules',
    'app.views',
    'app.lib',

    'django.contrib.admin',
)
###############################################################################
## Database Setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'portfolioAppDB',
        'USER': 'nickflorin',
        'PASSWORD': 'N1cholas!',
        'HOST': '10.13.0.29',
        'PORT': '5432',
        'CONN_MAX_AGE':100,
    }
}

###############################################################################
# Configure templates
TEMPLATES = [  
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
'django.middleware.common.CommonMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'app.nocache.NoCache',
)

#############################################################################
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
      os.path.join(BASE_DIR, 'assets'),
)  

STATICFILES_FINDERS = (
   'django.contrib.staticfiles.finders.FileSystemFinder',
   'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

