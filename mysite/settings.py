# Django settings for mysite project.

import os
from silversupport.env import is_production
from silversupport.secret import get_secret

if not is_production():
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Ryan Shaw', 'ryanshaw@unc.edu'),
)

DEFAULT_FROM_EMAIL = 'Ryan Shaw <ryanshaw@unc.edu>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
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
TIME_ZONE = 'US/Eastern'

LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

MEDIA_ROOT = os.environ['CONFIG_FILES']
MEDIA_URL = '/files/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/loggedin/'
LOGOUT_URL = '/logout/'

SECRET_KEY = get_secret()

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'mysite.middleware.ShortURLMiddleware',
    'mysite.middleware.XUACompatibleMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
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
    'django.contrib.flatpages',
    'south',
    'shorturls',
    'mysite.shared',
    'mysite.blog',
    'mysite.courses',
    'mysite.comments',
    'mysite.talking',
    'mysite.files',
)

COMMENTS_APP = 'mysite.comments'

SHORT_BASE_URL = 'http://aesh.in/'
SHORTEN_FULL_BASE_URL = 'http://aeshin.org/'
SHORTEN_MODELS = {
    'T': 'reading.text',
    'S': 'talking.talk',
    'R': 'flatpages.flatpage',
}

#HAYSTACK_SITECONF = 'mysite.search_sites'
#HAYSTACK_SEARCH_ENGINE = 'xapian'
#HAYSTACK_XAPIAN_PATH = os.path.join(os.environ['CONFIG_FILES'], 'mysite.index')

ZOTERO_GROUP_ID = '51755'

from secrets import *
