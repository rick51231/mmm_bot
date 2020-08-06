import os
from datetime import timedelta

import environ
from celery.schedules import crontab

from core.utils.base import get_settings_path

env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
environ.Env.read_env(get_settings_path(CONFIG_DIR, ('production.env', 'sandbox.env', 'local.env')))

SECRET_KEY = env('SECRET_KEY')
CF_EMAIL = env.str('CF_Email', default="")
CF_KEY = env.str('CF_Key', default="")

DEBUG = env.bool('DEBUG', default=True)
IS_PRODUCTION = env.bool("IS_PRODUCTION", default=False)
VIDEO_DATA_SELECT = env.dict("VIDEO_DATA_SELECT")
VIDEO_STEP_1 = env.str("VIDEO_STEP_1")
VIDEO_STEP_2 = env.str("VIDEO_STEP_2")
VIDEO_STEP_3 = env.str("VIDEO_STEP_3")
COMPANY_URL = env.str("COMPANY_URL")
TEXT_STEP_1 = env.str("TEXT_STEP_1")
TEXT_STEP_2 = env.str("TEXT_STEP_2")
TEXT_STEP_4 = env.str("TEXT_STEP_4")

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': env.db("DATABASE_URL")
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = "/static/"

# TRANSPORT
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ("workers.task",)

CELERY_BEAT_SCHEDULE = {
    'send_notification_users': {
        'task': 'workers.task.send_notification_users',
        'schedule': timedelta(minutes=1),
    },
}
