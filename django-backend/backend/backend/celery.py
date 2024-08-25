from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'close-timeout-payments': {
        'task': 'shop:close-timeout-payments:task',
        'schedule': crontab(minute=0, hour='*/3'),
        'options': {'queue': 'celery'},
    },
    'deactivate-expired-subscriptions': {
        'task': 'profile:deactivate-expired-subscriptions:task',
        'schedule': crontab(minute=0, hour='*/5'),
        'options': {'queue': 'celery'},
    },
    'distribution-of-free-token': {
        'task': 'profile:distribution-of-free-token:task',
        'schedule': crontab(minute=0, hour=0),
        'options': {'queue': 'celery'},
    },
    'close-timeout-jobs': {
        'task': 'jobs:close-timeout-jobs:task',
        'schedule': crontab(minute='*/5'),
        'options': {'queue': 'celery'},
    },
    'close-success-inst-jobs': {
        'task': 'jobs:close-success-inst-jobs:task',
        'schedule': crontab(minute='*/10'),
        'options': {'queue': 'celery'},
    },
    'close-timeout-messages': {
        'task': 'mailing:close-expired-mailing:task',
        'schedule': crontab(minute='*/60'),
        'options': {'queue': 'celery'},
    },
    'patreon-checker': {
        'task': 'shop:check_patreon_subscription:task',
        'schedule': crontab(minute='*/10'),
        'options': {'queue': 'celery'},
    },
    'face2img:close-timeout-jobs:task': {
        'task': 'face2img:close-timeout-jobs:task',
        'schedule': crontab(minute='*/5'),
        'options': {'queue': 'celery'},
    }
    # 'resend-mailing-messages': {
    #     'task': 'mailing:resend-message:task',
    #     'schedule': crontab(minute='*/15'),
    #     'options': {'queue': 'celery'},
    # },
    # 'delete-blur-images': {
    #     'task': 'jobs:delete-blur-images:task',
    #     'schedule': crontab(minute=0, hour='*/5'),
    # },
    # 'delete-undress-images': {
    #     'task': 'jobs:delete-undress-images:task',
    #     'schedule': crontab(minute=0, hour='*/24'),
    # },
}

app.autodiscover_tasks()
