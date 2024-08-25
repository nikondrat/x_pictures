from __future__ import absolute_import

import os
from pathlib import Path

DEBUG = True

ELASTICSEARCH_DSL = {}
SECRET_KEY = 'django-insecure--ilk)1=^ogfw-ix#q$u8d-c$rhd+*^(1pe=&k8$pr7kc%^7exo'

ROOT_DIR = Path(__file__).parent.parent.parent.parent
BASE_DIR = ROOT_DIR / 'backend'

RABBITMQ_URL = 'amqp://guest:guest@rabbitmq:5672'
REDIS_URL = 'redis://redis:6379/'

CELERY_BROKER_URL = RABBITMQ_URL
CELERY_RESULT_BACKEND = REDIS_URL + '2'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'backend',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'x-dev-database',
        'PORT': 5432,
    }
}

NGROK_DOMAIN = os.getenv('NGROK_DOMAIN')
