###############################################
# Tehorng main settings.
###############################################
import os, sys
from os.path import join as pjoin

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

sys.path.append(pjoin(PROJECT_PATH, 'apps'))

DEBUG = False
TEMPLATE_DEBUG = DEBUG 

ADMINS = (
     ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', #'postgresql_psycopg2',
        'NAME': pjoin(PROJECT_PATH, 'tehorngdev.db'), #'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_pass',
    }
}

TIME_ZONE = 'America/Toronto'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False #possibly later 

USE_L10N = True

MEDIA_ROOT = pjoin(PROJECT_PATH, 'media') 

MEDIA_URL = '/media/'

STATIC_ROOT = pjoin(PROJECT_PATH, 'static')

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'MAKE A UNIQUE RANDOM KEY HERE'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #Handle Banned IP/Users
    'tracking.middleware.BannedMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware',
    #Pagination
    'pagination.middleware.PaginationMiddleware',
    #Online
    'accounts.middleware.OnlineUserMiddleware',
    #FlatPage fallback.
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    #User Messaging
    'messaging.context_processors.user_messages',
    #Online Users
    'accounts.context_processors.online',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (pjoin(PROJECT_PATH, 'templates'))

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.humanize',
    'accounts',
    'submissions',
    'messaging',
    'blog',
    'contact',
    'search',
    'updates',
    'tracking',
    'reporting',
    'polls',
    'activity',
    'issues',
    #'history',
    #3rd Party
    'forum',
    #'reversion',
    'haystack',
    'gravatar',
    'django_extensions',
    'tagging',
    'sorl.thumbnail',
    'smileys',
    'south',
    'pagination',
    #'indexer',
    'paging',
    #'sentry',
    #'sentry.client',
    'voting',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

HAYSTACK_SITECONF = "tehorng_search"
HAYSTACK_SEARCH_ENGINE = "xapian"
HAYSTACK_XAPIAN_PATH = pjoin(PROJECT_PATH, "xapian")

DEFAULT_FROM_EMAIL = 'your_email@domain.com'
SERVER_EMAIL = "your_email@domain.com"

EMAIL_SUBJECT_PREFIX = "[Subject Prefix] "

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_DOMAIN = 'your domain'
SESSION_COOKIE_NAME = 'your cookie name'

FORCE_LOWERCASE_TAGS = True 

CACHE_BACKEND = "memcached://127.0.0.1:11211/"

HASH_TRACKING_SALT = "random string"

RECAPTCHA_PUBLIC_KEY = "recaptcha pub key"
RECAPTCHA_PRIVATE_KEY = "recaptcha private key"


LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/accounts/profile/'

#Load instatalltion specific settings/passwords.
execfile(pjoin(PROJECT_PATH,'.private-settings'))

