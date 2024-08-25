from __future__ import absolute_import

import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent
BASE_DIR = ROOT_DIR / 'backend'

CONFIG_DIR = BASE_DIR / 'config'
WATERMARK_IMAGE_PATH = CONFIG_DIR / 'watermark.png'
BOOKS_DIR = CONFIG_DIR / 'books'

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CSRF_TRUSTED_ORIGINS = ['*']
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http[s]?://.+$",
]

DOMAIN = os.getenv('DOMAIN', 'https://api-stage.x-pictures.io/')
SHOP_DOMAIN = os.getenv('SHOP_DOMAIN', 'https://api.x-shop.club/')

FRONT_DOMAIN = os.getenv('FRONT_DOMAIN', 'https://x-pictures.io/')
FRONT_SHOP_DOMAIN = os.getenv('FRONT_SHOP_DOMAIN', 'https://x-shop.club/')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_elasticsearch_dsl',
    'corsheaders',
    'rest_framework',
    'drf_spectacular',
    'storages',
    'django_admin_listfilter_dropdown',
    'rangefilter',

    'core.users',
    'core.common',

    'apps.accounts',
    'apps.subscriptions',
    'apps.hub',
    'apps.payments',
    'apps.support',

    # V2
    'apps.shop',
    'apps.profiles',
    'apps.jobs',
    'apps.telegram',
    'apps.gallery',
    'apps.mailing',
    'apps.face2img',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

RABBITMQ_URL = os.getenv('RABBITMQ_URL', '')
REDIS_URL = os.getenv('REDIS_URL', '')

ML_CALLBACK_QUEUE = 'ml:queue:callback'
ML_UNDRESS_QUEUE = 'ml:undress:queue'
ML_GENERATE_QUEUE = 'ml:generate:queue'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DEFAULT_DATABASE_NAME'),
        'USER': os.getenv('DEFAULT_DATABASE_USERNAME'),
        'PASSWORD': os.getenv('DEFAULT_DATABASE_PASSWORD'),
        'HOST': os.getenv('DEFAULT_DATABASE_HOST'),
        'PORT': os.getenv('DEFAULT_DATABASE_PORT'),
    }
}

ELASTICSEARCH_USER = os.getenv('ELASTICSEARCH_USER')
ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD')
ELASTICSEARCH_HTTP_AUTH = None
if ELASTICSEARCH_USER and ELASTICSEARCH_PASSWORD:
    ELASTICSEARCH_HTTP_AUTH = (ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD)

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.getenv('ELASTICSEARCH_HOST'),
        'http_auth': ELASTICSEARCH_HTTP_AUTH,
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


LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('ru', 'Русский'),
    ('en', 'English'),
    ('de', 'Deutsch'),
    ('es', 'Español'),
    ('fr', 'Français'),

    ('it', 'Italiano'),
    ('ja', '日本語'),
    ('pl', 'Polski'),
)

LANGUAGES_CONFIG = {
    'ru': ('ru', 'en',),
    'default': ('en', 'ru',)
}

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY_ID')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_DEFAULT_REGION}.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

STATICFILES_STORAGE = 'core.common.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'core.common.storage_backends.PublicMediaStorage'

AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

ALLOWED_IPS = (
    os.getenv('ALLOWED_IP_1'),
)
ACCESS_TOKENS = (
    os.getenv('ACCESS_TOKEN_1'),
)

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'core.common.throttling.BackedScopedRateThrottle',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'register': '50/day',
        'login': '100/min',
    },
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.users.authentication.ApiTokenAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'UNICODE_JSON': True,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'X-Pictures API',
    'VERSION': '2.2.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'DEFAULT_GENERATOR_CLASS': 'core.common.openapi.generators.CustomSchemaGenerator',
    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.AllowAny'
    ],
    'SCHEMA_PATH_PREFIX': r'/api/',
    'SERVE_AUTHENTICATION': (),
    'COMPONENT_SPLIT_REQUEST': True,
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

CELERY_BROKER_URL = RABBITMQ_URL
CELERY_RESULT_BACKEND = REDIS_URL + '2'
CELERY_BROKER_CONNECTION_TIMEOUT = 3
CELERY_BROKER_CONNECTION_MAX_RETRIES = 10
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'UTC'
CELERY_IGNORE_RESULT = True
CELERY_TASK_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['json']

IVENDPAY_API_KEY = os.getenv('IVENDPAY_API_KEY')

PAYPAL_TEST = False
PAYPAL_WEBHOOK_ID = '0T691308T2131125H'
PAYPAL_CLIENT_ID = 'AZYWZLotVTSgodxe4LFdpiEY8SAbbBwofm9-TDCFWiqbDulFVd0fxZBPr9BKY01auZcwdIFNNdhOifQB'
PAYPAL_SECRET_KEY = 'EK1BlRV6G7N8RNS7Q6b-3hgVmvOohw1z2mJuNGUROnUZKw0ZUUgT1cVaPAMHI_rPsZdh_oI1QIPLNhx1'
# PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
# PAYPAL_SECRET_KEY = os.getenv('PAYPAL_SECRET_KEY')

PAYADMIT_TEST = False
PAYADMIT_SECRET_KEY = os.getenv('PAYADMIT_SECRET_KEY')
PAYADMIT_SIGNING_KEY = os.getenv('PAYADMIT_SIGNING_KEY', '22DXC1cqkqmH')
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
STRIPE_WEBHOOK_KEY = os.getenv('STRIPE_WEBHOOK_KEY')

TAPFILIATE_API_KEY = os.getenv('TAPFILIATE_API_KEY')

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET_KEY = os.getenv('GOOGLE_CLIENT_SECRET_KEY')
GOOGLE_REDIRECT_URI = 'postmessage'

SOCIAL_SECRET = os.getenv('SOCIAL_SECRET')

TELEGRAM_BOTS = {
    'payment-notify': {
        'api_key': '6450230355:AAHSapd4iFhgaHKb3RSuzOciJy5PVzFznro',
        'admin_chat_ids': [
            5280824843,
            688225742,
            5255512400,
            112081305,
        ]
    }
}

NOVITA_CLIENT_API_KEY = os.getenv('NOVITA_CLIENT_API_KEY')

MASK_BUILDER_URL = os.getenv('MASK_BUILDER_URL')
MASK_BUILDER_SECRET_CODE = os.getenv('MASK_BUILDER_SECRET_CODE')

INSTAGRAM_PARSER_URL = os.getenv('INSTAGRAM_PARSER_URL')
INSTAGRAM_PARSER_SCODE = os.getenv('INSTAGRAM_PARSER_SCODE')

USE_GENERATE_NOVITA = True
USE_UNDRESS_NOVITA = True

ARK_PAY_API_KEY = os.getenv('ARK_PAY_API_KEY')
ARK_PAY_SECRET_KEY = os.getenv('ARK_PAY_SECRET_KEY')

# For moviepy
# os.environ['IMAGEIO_FFMPEG_EXE'] = '/usr/bin/ffmpeg'

ADD_IMAGE_TO_GALLERY = True
ADD_VIDEO_TO_GALLERY = True

PATREON_CLIENT_ID = 'kq2Uuk9X1QzdAbauo7cMxC-y4SsjsFe3Q9g9KmBfDLGou1C6W1SzKdylnqT1JSdD'
PATREON_CLIENT_SECRET_KEY = 'CZpG0fJO0CntBqrst2duqjM2t8jf7TZuAD0hb7RI51hFEJ3RkTcfMbMcqkf8FnXE'
PATREON_CAMPAIGN_ID = 11997471
PATREON_REDIRECT_URI = 'https://www.x-pictures.io/'
