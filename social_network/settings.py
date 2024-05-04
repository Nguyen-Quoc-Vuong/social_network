"""
Django settings for social_network project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR /'.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tq@z^zzy63%i6(+)=4l6vr2-g2p^#ba6&*-$u3b)d(bjb&(evb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'chat.apps.ChatConfig',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # pip install djangorestframework
    'corsheaders', # pip install django-cors-headers
    'django_mongoengine',
    # 'debug_toolbar',
    'homepage',
    'users',
    'posts',
    # 'chat',
    'comments',
    'reactions',
    'friends',
    'userprofiles',
    'channels',
    'mess',
    'navbar',
    'notifications',
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'social_network.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'social_network.wsgi.application'

ASGI_APPLICATION = "social_network.asgi.application"

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
    "redis": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'social_network',
        'USER': 'admin',
        'PASSWORD': 'abc123',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}

MONGODB_DATABASES = {
    "default": {
        "name": "social_network",
        "host": "localhost",
        "port": 27017,
        # "username": "mongo_user",  # replace with your username
        # "password": "mongo_password",  # replace with your password
    }
}

# CACHES = {
#     "default" : {
#         "BACKEND" : "django_redis.cache.RedisCache",
#         "LOCATION" : "redis://0.0.0.0:6379",
#         "OPTIONS" : {
#             "CLIENT_CLASS" : "django_redis.client.DefaultClient"
#         } 
#     }
# }

import mongoengine

mongoengine.connect(
    db='social_network',
    host='mongodb://localhost/social_network'
)

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

STATICFILES_DIRS =  (os.path.join(BASE_DIR, 'users\\static'),
                    os.path.join(BASE_DIR, 'userprofiles\\static'),
                    os.path.join(BASE_DIR, 'posts\\static'),
                    os.path.join(BASE_DIR, 'friends\\static'),
                    os.path.join(BASE_DIR, 'homepage\\static'),
                    os.path.join(BASE_DIR, 'comments\\static'),
                    os.path.join(BASE_DIR, 'reactions\\static'),
                    os.path.join(BASE_DIR, 'navbar\\static'),

)

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH_USER_MODEL = 'users.User'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# logging setting
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "mytype": {
            "format": "{asctime}:{levelname} - {name} {module}.py (line {lineno:d}). {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": env('DJANGO_LOG_FILE'),
            "level": env('DJANGO_LOG_LEVEL'),
            "formatter": "mytype",
        },
        'logtail': {
            'class': 'logtail.LogtailHandler',
            'source_token': env('BETTERSTACK_SOURCE_TOKEN'),
        },
        # "console": {
        #     "class": "logging.StreamHandler",
        #     "level": "DEBUG",
        #     "formatter": "mytype",
        # }
    },
    "loggers": {
        "users.views": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "userprofiles.views": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "userprofiles.viewsEdit": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "reactions.views": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "notifications.views": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "navbar.views": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "mess.views": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "homepage.views": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "friends.views": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "comments.views": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "chat.views": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
        "users.models": {
            "handlers": ["logtail", "file"],
            "level": env('DJANGO_LOG_LEVEL'),
            "propagate": False,
        },
    },
}