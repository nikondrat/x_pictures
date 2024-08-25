import json

import pika

from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand

from core.common import get_logger
from apps.jobs.services import after_work_service

logger = get_logger('save-ml-images:daemon')


class Command(BaseCommand):
    @transaction.atomic()
    def callback(self, ch, method, properties: pika.BasicProperties, body):
        message = json.loads(body)

        after_work_service(
            pk=properties.correlation_id,
            job_type=message['job_type'],
            result=message
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(
            queue=settings.ML_CALLBACK_QUEUE,
            durable=True,
        )

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=settings.ML_CALLBACK_QUEUE,
            on_message_callback=self.callback,
        )
        logger.info('[*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
