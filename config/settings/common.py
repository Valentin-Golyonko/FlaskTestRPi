import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

from app.core.choices import Choices

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # /<some_path>/HomeBox

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_celery_beat',
    'crispy_forms',
    'django_extensions',

    'app.core',
    'app.barometer',
    'app.owm_forecast',
    'app.alarm',
    'app.rgb_control',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static/homebox/']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Celery settings ->
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', default=None)
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND', default=None)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_IMPORTS = (
    'app.core.tasks',
    'app.barometer.tasks',
    'app.owm_forecast.tasks',
)

CELERY_BEAT_SCHEDULE = {
    'request-barometer-data': {
        'task': 'app.barometer.tasks.task_request_barometer_data',
        'schedule': crontab(minute=f"*/{Choices.BAROMETER_UPDATE_PERIOD}"),
    },
    'request-forecast-data': {
        'task': 'app.owm_forecast.tasks.task_request_owm_data',
        'schedule': crontab(minute=f"*/{Choices.FORECAST_UPDATE_PERIOD}"),
    },
}
# <- Celery settings

# Django rest
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_PARSER_CLASSES': (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Django logging
DJANGO_LOG_LEVEL = 'WARNING'
APP_LOG_LVL = 'DEBUG'
LOGS_DIR = 'logs/'
FILE_DJANGO = BASE_DIR / LOGS_DIR / 'django.log'
FILE_DEBUG = BASE_DIR / LOGS_DIR / 'debug.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} | {asctime} | {module} | {message}.',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} | {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_django': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 10,
            'filename': FILE_DJANGO,
            'formatter': 'verbose',
        },
        'file': {
            'level': APP_LOG_LVL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 10,
            'filename': FILE_DEBUG,
            'formatter': 'verbose',
        },
        'console': {
            'level': APP_LOG_LVL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_django', 'console'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': True,
        },
        'app.core': {
            'handlers': ['file', 'console'],
            'level': APP_LOG_LVL,
            'propagate': True,
        },
        'app.barometer': {
            'handlers': ['file', 'console'],
            'level': APP_LOG_LVL,
            'propagate': True,
        },
        'app.owm_forecast': {
            'handlers': ['file', 'console'],
            'level': APP_LOG_LVL,
            'propagate': True,
        },
    },
}

# Send email Google
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = 1
EMAIL_USE_SSL = 0
EMAIL_PORT = 587

LOGOUT_REDIRECT_URL = 'login'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
}

SESSION_COOKIE_AGE = 600  # 10 min
SESSION_SAVE_EVERY_REQUEST = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
