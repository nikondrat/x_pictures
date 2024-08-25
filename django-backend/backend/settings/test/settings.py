from __future__ import absolute_import

import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent
BASE_DIR = ROOT_DIR / 'backend'
CONFIG_DIR = BASE_DIR / 'config'


SECRET_KEY = 'test-secret'

UNISENDER_URL = 'https://test-url/'
UNISENDER_API_KEY = 'test-api-key'
UNISENDER_FROM_EMAIL = 'unisender-email@email.com'

ACCESS_TOKENS = (
    'access-token:7efb9379956551184eca451ff14884cf4983eb23',
    'access-token:8a17de6471af6cb0c8c1dc3707c29a256a7bb473',
)

ALLOWED_IPS = (
    '127.0.0.0',
)

CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'

PAYPAL_CLIENT_ID = '241'
PAYPAL_SECRET_KEY = '123'

AWS_STORAGE_BUCKET_NAME = 'x-pictures-backend-static'
AWS_DEFAULT_REGION = 'us-east-2'
AWS_ACCESS_KEY_ID = 'AKIAXH7CTJ33CBLL722I'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_DEFAULT_REGION}.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

STATICFILES_STORAGE = 'core.common.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'core.common.storage_backends.PublicMediaStorage'

AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

INSTAGRAM_PARSER_URL = 'https://insta-parser-test/'
INSTAGRAM_PARSER_SCODE = 1234

ELASTICSEARCH_DSL_AUTOSYNC = False
