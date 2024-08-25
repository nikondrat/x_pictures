from django.utils import timezone

import factory.fuzzy
from factory.django import DjangoModelFactory

from core.users.factories import UserFactory

from apps.subscriptions import models
from apps.subscriptions import services


class UserSubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = models.UserSubscription

    user_id = factory.LazyAttribute(lambda _: UserFactory().id)
    active = True

    class Params:
        current_free = factory.Trait(
            subscription_id=1,
            start_period=timezone.now(),
            end_period=timezone.now() + services.FreeSubscriptionService.life_time,
        )
        current_basic = factory.Trait(
            subscription_id=2,
            start_period=timezone.now(),
            end_period=timezone.now() + services.BasicSubscriptionService.life_time,
        )
        current_premium = factory.Trait(
            subscription_id=3,
            start_period=timezone.now(),
            end_period=timezone.now() + services.PremiumSubscriptionService.life_time,
        )
