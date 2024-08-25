import factory.fuzzy
from factory.django import DjangoModelFactory

from core.users.factories import UserFactory
from apps.profiles import models


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = models.Profile

    owner = factory.LazyAttribute(lambda _: UserFactory())
    balance = 0
    type = models.ProfileType.basic


class ProfileSubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = models.ProfileSubscription

    profile = factory.LazyAttribute(lambda _: ProfileFactory())
