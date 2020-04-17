import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')

# Redis uri for caching, celery, etc...

REDIS_URI = os.environ.get('REDIS_URI')


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        "PASSWORD": os.environ.get("SQL_PASSWORD",),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
    }
}

# Sessions

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Caching

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URI,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': 'portfolio_'
    }
}

CELERY_BROKER_URL = REDIS_URI
CELERY_RESULT_BACKEND = REDIS_URI

# Static settings

STATIC_ROOT = '/staticfiles/'
MEDIA_ROOT = '/mediafiles/'

# SSL

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
