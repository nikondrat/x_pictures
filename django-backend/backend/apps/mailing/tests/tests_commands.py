from datetime import timedelta

import pytest

from django.utils import timezone

from core.users.factories import UserFactory
from apps.mailing.models import Message, Event


@pytest.mark.django_db
def test_first_event_2024_command(mocker):
    from apps.mailing.management.commands.first_event_2024 import Command

    def mock_send_task(name: str, kwargs: dict):
        assert name == 'send-message:task'
        assert kwargs.get('message_id') is not None

    mocker.patch(
        'core.users.services.current_app.send_task',
        new=mock_send_task
    )

    user1 = UserFactory(
        date_joined=timezone.now() - timedelta(days=16)
    )
    user2 = UserFactory(
        date_joined=timezone.now() - timedelta(days=1),
    )
    user3 = UserFactory(
        date_joined=timezone.now() - timedelta(days=7),
    )

    Command().handle()

    assert Message.objects.filter(user=user1).first() is None

    message2 = Message.objects.get(user=user2)
    assert message2.status == Message.Status.CREATED
    assert message2.event == Event.first_event_2024

    message3 = Message.objects.get(user=user3)
    assert message3.status == Message.Status.CREATED
    assert message3.event == Event.first_event_2024
