# Django settings for mysite project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Ryan Shaw', 'ryanshaw@unc.edu'),
)

DEFAULT_FROM_EMAIL = 'Ryan Shaw <ryanshaw@unc.edu>'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ryan.b.shaw@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.environ['CONFIG_FILES'], 'mysite.db')
    }
}

# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
TIME_ZONE = None

LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

MEDIA_ROOT = os.environ['CONFIG_WRITABLE_ROOT']
MEDIA_URL = '/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
LOGIN_REDIRECT_URL = '/loggedin/'

from silversupport.secret import get_secret
SECRET_KEY = get_secret()

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.comments',
    'south',
    #'haystack',
    'mysite.shared',
    'mysite.blog',
    'mysite.courses',
)

#HAYSTACK_SITECONF = 'mysite.search_sites'
#HAYSTACK_SEARCH_ENGINE = 'xapian'
#HAYSTACK_XAPIAN_PATH = os.path.join(os.environ['CONFIG_FILES'], 'mysite.index')

from secrets import *
