import uuid

import factory.fuzzy
from factory.django import DjangoModelFactory

from core.users.factories import UserFactory

from apps.accounts import models


class UndressJobFactory(DjangoModelFactory):
    class Meta:
        model = models.UndressJob

    id = factory.LazyAttribute(lambda _: uuid.uuid4())
    user_id = factory.LazyAttribute(lambda _: UserFactory().id)

    class Params:
        admin = factory.Trait(
            image_url=factory.Faker('url'),
        )


class GenerationJobFactory(DjangoModelFactory):
    class Meta:
        model = models.GenerationJob

    id = factory.LazyAttribute(lambda _: uuid.uuid4())
    user_id = factory.LazyAttribute(lambda _: UserFactory().id)
    image_url = factory.Faker('url')
    prompt = 'sex'

    class Params:
        admin = factory.Trait(
            image_url=factory.Faker('url'),
        )
