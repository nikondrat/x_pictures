from celery import shared_task, current_app

from django.core import mail
from django.conf import settings
from django.utils import timezone

from core.common.utils import get_logger
from apps.mailing.models import Message
from apps.mailing.services import get_event

logger = get_logger('mailing:tasks')


@shared_task(name='mailing:close-expired-mailing:task')
def close_expired_mailing_task():
    Message.objects.filter(
        expiry_at__lte=timezone.now()
    ).update(
        status=Message.Status.EXPIRED,
    )


@shared_task(name='send-message:task')
def send_message(message_id: int):
    message = Message.objects.get(id=message_id)
    if message.status != Message.Status.CREATED:
        return True

    event = get_event(message=message)
    subject, html_message, plain_message = event.make_message(message=message)

    email = mail.EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[message.user.email],
        connection=mail.get_connection(),
    )
    email.attach_alternative(html_message, 'text/html')

    message.status = Message.Status.SENT
    message.expiry_at = timezone.now() + event.lifetime
    message.save()
    try:
        return email.send()
    except Exception as err:
        logger.error(f'{err}')
        return False


@shared_task(name='mailing:resend-message:task')
def resend_messages():
    messages = Message.objects.filter(status=Message.Status.CREATED)[:10]
    for message in messages:
        current_app.send_task(
            'send-message:task',
            kwargs={'message_id': message.pk},
        )
