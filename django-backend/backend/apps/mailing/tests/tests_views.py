from datetime import timedelta

import pytest

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.mailing.models import Message, Event
from apps.profiles.models import Profile
from apps.profiles.factories import ProfileFactory


@pytest.mark.django_db
class TestFirstEvent2024:

    def test_first_event_2024_view_success(self, api_client):
        profile1 = ProfileFactory(balance=0)
        profile2 = ProfileFactory(balance=3)

        message1 = Message.objects.create(
            user=profile1.owner,
            event=Event.first_event_2024,
            status=Message.Status.SENT,
            expiry_at=timezone.now() + timedelta(days=3),
        )
        message2 = Message.objects.create(
            user=profile1.owner,
            event=Event.first_event_2024,
            status=Message.Status.SENT,
            expiry_at=timezone.now() + timedelta(days=3),
        )

        assert message1.secret_code != message2.secret_code

        response1 = api_client.get(reverse('mailing:first_event_2024',
                                           kwargs={'secret_code': message1.secret_code}))
        response2 = api_client.get(reverse('mailing:first_event_2024',
                                           kwargs={'secret_code': message2.secret_code}))

        assert response1.status_code == status.HTTP_302_FOUND
        assert response2.status_code == status.HTTP_302_FOUND

        assert Message.objects.get(pk=message1.pk).status == Message.Status.SUCCESS
        assert Message.objects.get(pk=message2.pk).status == Message.Status.SUCCESS

        assert Profile.objects.get(pk=profile1.pk).balance == 2
        assert Profile.objects.get(pk=profile2.pk).balance == 3

    def test_first_event_2024_view_not_found(self, api_client):
        response1 = api_client.get(reverse('mailing:first_event_2024',
                                           kwargs={'secret_code': 'fasdfasd'}))
        assert response1.status_code == status.HTTP_302_FOUND

    def test_first_event_2024_view_expired(self, api_client):
        profile1 = ProfileFactory(balance=0)
        message1 = Message.objects.create(
            user=profile1.owner,
            event=Event.first_event_2024,
            status=Message.Status.SENT,
            expiry_at=timezone.now() - timedelta(days=3),
        )

        response1 = api_client.get(reverse('mailing:first_event_2024',
                                           kwargs={'secret_code': message1.secret_code}))
        assert response1.status_code == status.HTTP_302_FOUND

        assert Message.objects.get(pk=message1.pk).status == Message.Status.EXPIRED
        assert Profile.objects.get(pk=profile1.pk).balance == 0
