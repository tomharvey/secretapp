"""
Note about this ``settings.py``:
    This file contains all the usual default django settings.
    However, to make this more extensible and to hide certain settings
    from the public in the github project. A file called ``environment.py``
    must be created at the root level of this project. With a series of needed
    settings. See below for details
    
List of needed settings:
    # current working directory so settings are relative
    CWD = '/home/timjdavey/apps'
    
    # make up some key - mash the keyboard
    SECRET_KEY = '123abc'
    
    # database settings - see notes below for details
    DATABASE_*
    
    # facebook api confs (simply the keys provided from the app)
    FACEBOOK_API_KEY = 'x'
    FACEBOOK_SECRET_KEY = 'x'
    
    # Solr / Solango configs
    SOLR_SERVER = 'localhost:8080'
    SOLR_ROOT = '/usr/lib/tomcat6/data/solr'
    SOLR_SCHEMA_PATH = SOLR_ROOT + '/conf/schema.xml'
    SOLR_DATA_DIR = SOLR_ROOT + '/data'
    SEARCH_UPDATE_URL = "http://%s/solr/update" % SOLR_SERVER
    SEARCH_SELECT_URL = "http://%s/solr/select" % SOLR_SERVER
    SEARCH_PING_URLS = ["http://%s/solr/admin/ping" % SOLR_SERVER,]
"""
try:
    from environment import CWD
except:
    raise ImportError, "Please create environment.py file in your base directory - see settings.py for details"

# Django settings for secret project.

ADMIN_INSERT = True # This will only be true while we load the data
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/London'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/templates/static/' % CWD

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/%smedia/' % MEDIA_URL

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "utilz.context_processors.settings",
    "utilz.context_processors.member_level",
    "utilz.context_processors.ajax",
)


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'socialauth.auth_backends.OpenIdBackend',
    #'socialauth.auth_backends.TwitterBackend',
    'perm.backends.ClaimFacebookBackend',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # facebook middleware, checks auth and gets info
    'facebook.djangofb.FacebookMiddleware',
    # gives a user a permission_level (see `perm` module)
    'perm.middleware.PermissionUserMiddleware',
    # adds additional data to user object
    'accounts.middleware.AugmentAccountMiddleware',
    # makes ajax responses pretty
    'utilz.middleware.AjaxExceptionResponse',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    "%s/templates/" % CWD,
)

# Solr configs. Please make sure SOLR_ROOT, SOLR_SERVER are defined in `environment.py`
from environment import SOLR_ROOT, SOLR_SERVER
SOLR_SCHEMA_PATH = '%s/conf/schema.xml' % SOLR_ROOT
SOLR_DATA_DIR = '%s/data' % SOLR_ROOT
SEARCH_UPDATE_URL = "http://%s/solr/update" % SOLR_SERVER
SEARCH_SELECT_URL = "http://%s/solr/select" % SOLR_SERVER
SEARCH_PING_URLS = ("http://%s/solr/admin/ping" % SOLR_SERVER,)


INSTALLED_APPS = (
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # dependancies
    'socialauth',
    'openid_consumer',
    'solango',
    'south',
    # internal
    'accounts',
    'comment',
    'perm',
    'discussion',
    'secret',
    'utilz',
)

# see top of document for notes
from environment import *


