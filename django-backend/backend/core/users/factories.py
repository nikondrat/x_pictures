import uuid

from django.utils import timezone

import factory.fuzzy
from factory.django import DjangoModelFactory

from django.contrib.auth.hashers import make_password

from core.users import models


class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    id = factory.LazyAttribute(lambda _: models.generate_user_id(is_anonymous=False))
    username = None
    decoded_password = factory.Faker('password')
    password = factory.LazyAttribute(lambda _: make_password(_.decoded_password))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    is_staff = False
    email_confirmed = True
    email_before_delete = None
    deleted_account = False

    class Params:
        admin = factory.Trait(
            is_staff=True,
        )
        email_unconfirmed = factory.Trait(
            email_confirmed=False
        )


class EmailMessageFactory(DjangoModelFactory):
    class Meta:
        model = models.EmailMessage

    key = factory.LazyAttribute(lambda _: models.EmailMessage.generate_secret_key())
    user_id = factory.LazyAttribute(lambda _: UserFactory().pk)
    type = factory.fuzzy.FuzzyChoice(models.EmailMessage.MessageType)
    email = factory.Faker('email')


class TokenFactory(DjangoModelFactory):
    class Meta:
        model = models.Token

    key = factory.LazyAttribute(lambda _: models.Token.generate_key())
    user_id = factory.LazyAttribute(lambda _: UserFactory().id)
    created = factory.LazyAttribute(lambda _: timezone.now())


class AlanBaseFactory(DjangoModelFactory):
    class Meta:
        model = models.AlanBase

    user = factory.LazyAttribute(lambda _: UserFactory())
    click_id = factory.LazyAttribute(lambda _: str(uuid.uuid4()))
