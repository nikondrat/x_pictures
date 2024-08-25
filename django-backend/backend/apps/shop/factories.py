import uuid

import factory.fuzzy
from factory.django import DjangoModelFactory

from core.users.factories import UserFactory
from apps.shop import models


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = models.Product

    title = 'Premium'
    public_title = 'Premium'

    description = 'Premium description'
    public_description = 'Premium description'

    type = models.ProductType.one_time
    amount = 100

    class Params:
        subscription = factory.Trait(
            type=models.ProductType.subscription,
            lifetime=60 * 60 * 24 * 30
        )
        one_time = factory.Trait(
            type=models.ProductType.one_time,
        )


class PriceFactory(DjangoModelFactory):
    class Meta:
        model = models.Price

    price = 100
    product = factory.LazyAttribute(lambda _: PriceFactory())
    currency = factory.fuzzy.FuzzyChoice(models.Currency)


class PaymentOrderFactory(DjangoModelFactory):
    class Meta:
        model = models.PaymentOrder

    invoice_id = factory.LazyAttribute(lambda _: str(uuid.uuid4().hex))
    payment_url = factory.Faker('url')
    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    price = 9.9
    currency = models.Currency.USD
    gateway_type = models.GatewayType.ivendpay
