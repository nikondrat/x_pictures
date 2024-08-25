from datetime import timedelta

import pytest

from django.utils import timezone

from apps.mailing.models import Message, Event


@pytest.mark.django_db
def test_close_expired_mailing_task(send_celery_task, get_user):
    message1 = Message.objects.create(
        user=get_user(),
        event=Event.first_event_2024,
        status=Message.Status.SENT,
        expiry_at=timezone.now() + timedelta(days=3),
    )
    message2 = Message.objects.create(
        user=get_user(),
        event=Event.first_event_2024,
        status=Message.Status.SENT,
        expiry_at=timezone.now() + timedelta(minutes=2),
    )
    message3 = Message.objects.create(
        user=get_user(),
        event=Event.first_event_2024,
        status=Message.Status.SENT,
        expiry_at=timezone.now() - timedelta(minutes=2),
    )
    message4 = Message.objects.create(
        user=get_user(),
        event=Event.first_event_2024,
        status=Message.Status.SENT,
        expiry_at=timezone.now() - timedelta(minutes=2),
    )

    send_celery_task(
        'mailing:close-expired-mailing:task',
    )

    assert Message.objects.get(pk=message1.pk).status == Message.Status.SENT
    assert Message.objects.get(pk=message2.pk).status == Message.Status.SENT

    assert Message.objects.get(pk=message3.pk).status == Message.Status.EXPIRED
    assert Message.objects.get(pk=message4.pk).status == Message.Status.EXPIRED
