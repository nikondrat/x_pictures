import pytest

from apps.shop.models import Product
from apps.profiles.models import Profile, ProfileType
from apps.profiles.factories import ProfileFactory, ProfileSubscriptionFactory


@pytest.mark.django_db
@pytest.mark.parametrize('subscription_id, profile_type, deleted', [
    (1, ProfileType.advance, False),
    (2, ProfileType.advance, True),
    (3, ProfileType.premium, False),
    (4, ProfileType.premium, True),
    (5, ProfileType.super_premium, False),
])
def test_signal_active_subscription(subscription_id: int, profile_type: ProfileType, deleted: bool):
    profile = ProfileFactory()
    assert profile.type == ProfileType.basic

    subscription = Product.objects.get(id=subscription_id)

    profile_subscription = ProfileSubscriptionFactory(profile=profile, subscription=subscription,)

    assert Profile.objects.get(pk=profile.pk).type == profile_type

    if deleted:
        profile_subscription.delete()
    else:
        profile_subscription.is_active = False
        profile_subscription.save()

    assert Profile.objects.get(pk=profile.pk).type == ProfileType.basic
