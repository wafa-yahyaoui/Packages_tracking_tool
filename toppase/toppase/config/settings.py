"""
Django settings for toppase project.
"""

import os
import re
import logging

# balabla comment

########################
# SERVER CONFIGURATION #
########################

ENV_TYPE = os.environ.get('ENV_TYPE', 'localhost')

My_SERVER_URL_ = '127.0.0.1:8000'

IS_LOCAL = True if ENV_TYPE == 'localhost' else False

IS_PRODUCTION_LIKE = True if ENV_TYPE in ('production', 'staging') else False

HOST_NAME = 'https://www.toppase.com' if ENV_TYPE == 'production' \
    else 'https://preprod.toppase.com' if ENV_TYPE == 'staging' \
    else 'https://dev.toppase.com' if ENV_TYPE == 'dev' \
    else 'http://localhost:5000'

INTERNAL_IPS = ['127.0.0.1', ]

# This sendgrid API Key
API_KEY = "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"

########################
# MAIN DJANGO SETTINGS #
########################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if ENV_TYPE in ('production', 'staging') else True
# Site id
SITE_ID = 1

WSGI_APPLICATION = 'config.wsgi.application'

ROOT_URLCONF = 'config.urls'

###############
# Toppase Env #
###############

SITE_NAME = "Toppase.com"

#################
# SITE SECURITY #
#################

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY') if ENV_TYPE in ('production', 'staging') \
    else 'rrhdi0n#dd03p-ikr19+w5!8z8)epf(28%03l$6i(#@)$w*g8e'

CSRF_COOKIE_SECURE = True if ENV_TYPE in ('production', 'staging') else False

SESSION_COOKIE_SECURE = True if ENV_TYPE in ('production', 'staging') else False

USE_SSL = not IS_LOCAL

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') if IS_LOCAL else None

SECURE_SSL_REDIRECT = True if not IS_LOCAL else False

ALLOWED_HOSTS = ['toppase.com', 'www.toppase.com'] if ENV_TYPE == 'production' else ['*']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

#######################
# EMAIL CONFIGURATION #
#######################

EMAIL_USE_TLS = True

try:
    EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_PORT = 587
except KeyError:
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)

DEFAULT_FROM_EMAIL = 'Pierre de toppase %s <pmondares%s@toppase.com>' % (
    '%s ' % ENV_TYPE if ENV_TYPE != 'production' else '',
    '+%s' % ENV_TYPE if ENV_TYPE != 'production' else '',
)
if ENV_TYPE == 'production':
    ADMINS = (
        ('Toppase Admins', 'admins@toppase.com'),
    )
    MANAGERS = (
        ('Hamdi Toppase MANAGERS', 'hgdoura@toppase.com'),
        ('Moez Toppase MANAGERS', 'mmaamer@toppase.com'),
        ('Bilal Toppase MANAGERS', 'bnisb@toppase.com'),
    )
    SUPPORT_EMAIL = 'hello@toppase.com'
else:
    ADMINS = (
        ('Toppase Admins [Not prod]', 'admins+notprod@toppase.com'),
    )
    MANAGERS = (
        ('Hamdi Toppase MANAGERS [Not prod]', 'hgdoura+test@toppase.com'),
        ('Moez Toppase MANAGERS [Not prod]', 'mmaamer+test@toppase.com'),
        ('Bilal Toppase MANAGERS [Not prod]', 'bnisb+test@toppase.com'),
    )

    SUPPORT_ADMINS = 'admins+test@toppase.com'

    SUPPORT = 'hello+test@toppase.com'

################
# APPLICATIONS #
################

# Application definition
DJANGO_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

EXTENSION_APPS = [
    # django extensions
    'django_extensions',
    # API DRF
    'rest_framework',
    # Debug toolbar
    'debug_toolbar',
    'bootstrap3',
    'oauth2_provider',
    'django_celery_results',
]

PROJECT_APPS = [
    'apps.accounts',
    'apps.trackings',
    'apps.payments',
    'apps.design',
    'apps.abstract',

]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + EXTENSION_APPS

##############
# MIDDLEWARE #
##############

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

##########################
# STATIC AND MEDIA FILES #
##########################

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
]

DJANGO_STATICFILES = not IS_LOCAL

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_S3_REGION_NAME = 'eu-central-1'

AWS_S3_SIGNATURE_VERSION = 's3v4'

# AWS_QUERYSTRING_AUTH = False

AWS_S3_FILE_OVERWRITE = True

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'

AWS_IS_GZIPPED = True

STATIC_URL = "https://%s/static/" % AWS_S3_CUSTOM_DOMAIN

MEDIA_URL = "https://%s/media/" % AWS_S3_CUSTOM_DOMAIN

STATIC_ROOT = '/static/' if not IS_LOCAL else os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = '/media/' if not IS_LOCAL else os.path.join(BASE_DIR, 'media')

FILE_UPLOAD_PERMISSIONS = 0644

# One Year
STATIC_EXPIRATION_SECONDS = 31536000

###################
# TEMPLATE DJANGO #
###################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.normpath(os.path.join(BASE_DIR, 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.cores.context_processors.settings',
            ],
        },
    },
]

TEMPLATE_ACCESSIBLE_SETTINGS = (
    'HOST_NAME',
    'ENV_TYPE',
    'SITE_TITLE',
)

# MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
#######################
# PASSWORD VALIDATION #
#######################
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

########################
# Internationalization #
########################

# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

DATE_FORMAT = 'j N Y'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('fr', 'FR'),
    ('en', 'EN'),
]

LOCALE_PATHS = [
    os.path.normpath(os.path.join(BASE_DIR, 'locale')),

]

#######################
# USER AUTHENTICATION #
#######################

AUTH_USER_MODEL = "accounts.Member"

LOGIN_REDIRECT_URL = "/user/profile"

LOGIN_URL = "/user/login"

AUTHENTICATION_BACKENDS = (
    'apps.cores.auth_backends.AccountBackend',
)

############
# DATABASE #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'toppase',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'hoffa',
        'PASSWORD': 'wafa0000',
        'HOST': 'localhost',
        # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}
# TEST_DATABASE_NAME = os.path.join(BASE_DIR, 'db.sqlite3')

###########
# FIXTURE #
###########

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

#################
# DEBUG TOOLBAR #
#################

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False} if DEBUG else {}

####################
# GRAPPELLIE ADMIN #
####################

GRAPPELLI_ADMIN_TITLE = "TOPPASE ADMIN [Dev]" if IS_LOCAL else "TOPPASE ADMIN"

####################
# CELERY SCHEDULER #
####################

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


#########################
# CELERY_RESULT_BACKEND #
#########################

CELERY_RESULT_BACKEND = 'django-db'

############
# LOGGING #
###########

class isLocalLoggingFilter(logging.Filter):
    def filter(self, record):
        return IS_LOCAL


class isNotLocalLoggingFilter(logging.Filter):
    def filter(self, record):
        return not IS_LOCAL


class autoEnvLimit(logging.Filter):
    LIMITS = {  # Changeable
        'localhost': 'DEBUG',
        'dev': 'DEBUG',
        'staging': 'INFO',
        'production': 'INFO',
    }

    def __init__(self, *args, **kw):
        # get the number
        self.limit_level = getattr(
            logging, getattr(
                self.LIMITS, ENV_TYPE, 'DEBUG'))
        super(autoEnvLimit, self).__init__(*args, **kw)

    def filter(self, record):
        if record.levelno >= self.limit_level:
            return 1
        else:
            return 0


IGNORABLE_404_URLS = [
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
]

LOCAL_CONSOLE_LEVEL = 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(levelname)s %(asctime)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'is_local': {
            '()': isLocalLoggingFilter,
        },
        'is_not_local': {
            '()': isNotLocalLoggingFilter,
        },
        'auto_env_limit': {
            '()': autoEnvLimit,
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['auto_env_limit', ],
        },
        'console_local': {
            'level': LOCAL_CONSOLE_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['is_local',
                        'auto_env_limit', ],
        },
        'console_remote': {
            'level': os.environ.get('CONSOLE_LOGLEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['is_not_local',
                        'auto_env_limit', ],
        },
        'log_file_local': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.NullHandler',
            'filters': ['is_local',
                        'auto_env_limit', ],
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console_remote', 'console_local',
                         'log_file_local', ],
            'propagate': True
        },
    }
}

#########################
# Django_rest_framework #
#########################


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'}
}

OAUTH2_PROVIDER_APPLICATION_MODEL = 'accounts.Member'
