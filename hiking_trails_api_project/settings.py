"""
Django settings for hiking_trails_api_project project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
  DEBUG=(bool, True),
  ENVIRONMENT=(str, "PRODUCTION"),
  ALLOW_ALL_ORIGINS=(bool, False),
  ALLOWED_HOSTS=(list, []),
  ALLOWED_ORIGINS=(list, []),
  CSRF_TRUSTED_ORIGINS=(list, []),
  DATABASE_ENGINE=(str, "django.db.backends.sqlite3"),
  DATABASE_NAME=(str, BASE_DIR / "db.sqlite3"),
  DATABASE_USER=(str, ""),
  DATABASE_PASSWORD=(str, ""),
  DATABASE_HOST=(str, ""),
  DATABASE_PORT=(int, 5432),
  HEROKU_SETTINGS=(bool, False),
  SECRET_KEY=(str, "secret123")
)

environ.Env.read_env()

ENVIRONMENT = env.str("ENVIRONMENT")

DEBUG = env.bool("DEBUG")
ALLOWED_HOSTS = tuple(env.list("ALLOWED_HOSTS"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')


# ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'https://trails-api-thomas-basham.herokuapp.com']

# Application definition

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  "whitenoise.runserver_nostatic",  # Use this with whitenoise
  'django.contrib.staticfiles',

  'rest_framework',

  'hiking_trails_api',

  'crispy_forms',

]

MIDDLEWARE = [
  'whitenoise.middleware.WhiteNoiseMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hiking_trails_api_project.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
      BASE_DIR / 'templates'
    ],
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

WSGI_APPLICATION = 'hiking_trails_api_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
  "default": {
    "ENGINE": env.str("DATABASE_ENGINE"),
    "NAME": env.str("DATABASE_NAME"),
    "USER": env.str("DATABASE_USER"),
    "PASSWORD": env.str("DATABASE_PASSWORD"),
    "HOST": env.str("DATABASE_HOST"),
    "PORT": env.int("DATABASE_PORT"),
  }
}

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, "static/"),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
  "DEFAULT_PERMISSION_CLASSES": [
    "rest_framework.permissions.IsAuthenticatedOrReadOnly",
  ]
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# ************ HEROKU DEPLOYMENT *****************

# This module uses Heroku’s DATABASE_URL variable if it’s on Heroku,
# or it uses the DATABASE_URL we set in the .env file if we’re working locally.
# dotenv_file = os.path.join(BASE_DIR, ".env")
# if os.path.isfile(dotenv_file):
#     dotenv.load_dotenv(dotenv_file)

#  Add configuration for static files storage using whitenoise

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

CSRF_TRUSTED_ORIGINS = [
  'https://trails-api-thomas-basham.herokuapp.com',
]
# Use Database setttings from heroku postgres
# if env.bool('HEROKU_SETTINGS'):
#     django_heroku.settings(locals())

X_FRAME_OPTIONS = 'ALLOW-FROM https://thomasbashamportfolio.net'
