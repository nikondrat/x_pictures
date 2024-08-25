from celery import shared_task

from django.db import transaction
from core.common.utils import get_logger

logger = get_logger("users")


@shared_task(name='users:send_email_task')
def send_email_task(email_message_id: str):
    from django.core import mail
    from django.conf import settings
    from django.utils.html import strip_tags
    from django.template.loader import render_to_string
    from core.users.models import EmailMessage

    obj = EmailMessage.objects.get(pk=email_message_id)

    html_message = render_to_string(obj.template, {
        'token': obj.key,
        'user': obj.user,
        'domain': settings.DOMAIN,
        'front_domain': settings.FRONT_DOMAIN,
    })
    plain_message = strip_tags(html_message)

    try:
        with transaction.atomic():
            mail.send_mail(
                obj.subject, plain_message, obj.from_email,
                [obj.to_email], fail_silently=False,
                html_message=html_message,
            )
            obj.status = EmailMessage.Status.SENT
            obj.save()
    except Exception as err:
        logger.error(f"Error sent email task: {err}")
        return False
    return True
