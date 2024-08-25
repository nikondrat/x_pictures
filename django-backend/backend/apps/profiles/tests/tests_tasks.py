import decimal
from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from django.utils import timezone

from apps.shop.models import Product
from apps.profiles.models import Profile, ProfileSubscription, ProfileType
from apps.profiles.factories import ProfileFactory, ProfileSubscriptionFactory


@pytest.mark.django_db
@pytest.mark.skip('TODO call task')
@freeze_time(datetime(2023, 12, 10))
def test_deactivate_expired_subscriptions_task(send_celery_task):
    subscription = Product.objects.get(id=4)

    profile1 = ProfileFactory()
    profile1_subscription = ProfileSubscriptionFactory(
        profile=profile1,
        subscription=subscription,
        end_period=timezone.now() - timedelta(days=15)
    )
    assert Profile.objects.get(pk=profile1.pk).type == ProfileType.premium

    profile2 = ProfileFactory()
    profile2_subscription = ProfileSubscriptionFactory(
        profile=profile2,
        subscription=subscription,
        end_period=timezone.now() - timedelta(days=10)
    )
    assert Profile.objects.get(pk=profile2.pk).type == ProfileType.premium

    profile3 = ProfileFactory()
    profile3_subscription = ProfileSubscriptionFactory(
        profile=profile3,
        subscription=subscription,
        end_period=timezone.now() + timedelta(days=12)
    )
    assert Profile.objects.get(pk=profile3.pk).type == ProfileType.premium

    send_celery_task('profile:deactivate-expired-subscriptions:task')

    assert Profile.objects.get(pk=profile1.pk).type == ProfileType.basic
    assert not ProfileSubscription.objects.get(pk=profile1_subscription.pk).is_active

    assert Profile.objects.get(pk=profile2.pk).type == ProfileType.basic
    assert not ProfileSubscription.objects.get(pk=profile2_subscription.pk).is_active

    assert Profile.objects.get(pk=profile3.pk).type == ProfileType.premium
    assert ProfileSubscription.objects.get(pk=profile3_subscription.pk).is_active


@pytest.mark.django_db
def test_distribution_of_free_token_task(send_celery_task):
    profile1 = ProfileFactory(balance=0)
    profile2 = ProfileFactory(balance=0.8)
    profile3 = ProfileFactory(balance=1.2)
    profile4 = ProfileFactory(balance=1)
    profile5 = ProfileFactory(balance=2)

    send_celery_task('profile:distribution-of-free-token:task')

    assert Profile.objects.get(pk=profile1.pk).balance == decimal.Decimal('20')
    assert Profile.objects.get(pk=profile2.pk).balance == decimal.Decimal('20')
    assert Profile.objects.get(pk=profile3.pk).balance == decimal.Decimal('20')
    assert Profile.objects.get(pk=profile4.pk).balance == decimal.Decimal('20')
    assert Profile.objects.get(pk=profile5.pk).balance == decimal.Decimal('20')
