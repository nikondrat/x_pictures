from celery import current_app
from django.db import transaction

from core.users.models import EmailMessage


@transaction.atomic()
def resend_email(user_id: str, email: str, typ: EmailMessage.MessageType):
    qs = EmailMessage.objects.filter(
        user_id=user_id,
        type=typ,
        status__in=[
            EmailMessage.Status.CREATE, EmailMessage.Status.SENT,
        ],
    )

    if qs.exists():
        qs.update(status=EmailMessage.Status.CANCEL)

    send_email(user_id=user_id, typ=typ, email=email)


def send_email(user_id: str, email: str, typ: EmailMessage.MessageType):
    email_message = EmailMessage.objects.create(
        user_id=user_id,
        type=typ,
        email=email,
    )

    transaction.on_commit(
        lambda: current_app.send_task(
            'users:send_email_task',
            kwargs=dict(
                email_message_id=email_message.pk,
            ),
        )
    )
