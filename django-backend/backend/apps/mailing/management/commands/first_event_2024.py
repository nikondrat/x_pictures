from datetime import timedelta

from celery import current_app

from django.db import transaction
from django.utils import timezone
from django.core.management.base import BaseCommand

from core.common.utils import get_logger
from core.users.models import User
from apps.mailing.models import Message, Event

logger = get_logger('mailing:first_event_2024')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-e', '--email', type=str, help='email address')

    @transaction.atomic()
    def sender(self):
        users = User.objects.filter(
            email_confirmed=True,
            date_joined__gte=timezone.now() - timedelta(days=14),
            date_joined__lte=timezone.now(),
        )

        for user in users:
            message = Message.objects.create(
                user=user,
                event=Event.first_event_2024,
            )
            current_app.send_task(
                'send-message:task',
                kwargs=dict(
                    message_id=message.pk,
                )
            )

    @transaction.atomic()
    def single_sender(self, email: str):
        user = User.objects.get(email=email)
        message = Message.objects.create(user=user, event=Event.first_event_2024)
        current_app.send_task(
            'send-message:task',
            kwargs=dict(
                message_id=message.pk,
            )
        )

    def handle(self, *args, **options):
        if options.get('email'):
            self.single_sender(email=options['email'])
        else:
            self.sender()
