import pytest

from rest_framework import status
from django.db.utils import IntegrityError
from django.urls import reverse
from django.conf import settings

from core.users.factories import UserFactory
from apps.profiles.models import ProfileType, Profile, ProfileSubscription
from apps.profiles.factories import ProfileFactory, ProfileSubscriptionFactory
from apps.shop.models import Currency, ProductType, GatewayType, Product, Price, PaymentOrder
from apps.shop.factories import ProductFactory, PriceFactory, PaymentOrderFactory


@pytest.mark.django_db
def test_create_product_with_duplicate_price():
    product = ProductFactory(id=55)
    PriceFactory(pk=666, product=product, currency=Currency.USD)

    with pytest.raises(IntegrityError):
        PriceFactory(pk=111, product=product, currency=Currency.USD)


@pytest.mark.django_db
class TestProductAPIViewSet:
    endpoint_subscription = reverse('products_set-subscriptions')

    @pytest.fixture(autouse=True)
    def setup(self):
        Product.objects.all().delete()  # delete products

    @pytest.mark.skip('---')
    def test_get_subscription_products(self, api_client):
        product = ProductFactory(id=3, type=ProductType.subscription)

        product_usd_price = PriceFactory(pk=111, product=product, currency=Currency.USD, price=2)

        response_usd = api_client.get(self.endpoint_subscription + '?currency=usd')
        assert response_usd.status_code == status.HTTP_200_OK

        assert response_usd.json() == [{
            'id': product.id,
            'title': product.public_title,
            'description': product.public_description,
            'image': product.image,
            'price': '%.2f' % product_usd_price.price,
            'paypal_billing_plan_id': product_usd_price.paypal_billing_plan_id,
            'currency': product_usd_price.currency.label,
            'type': product.type,
            'amount': '%.2f' % product.amount,
            'lifetime': product.lifetime,
            'lifetime_type': 'month',
        }]


@pytest.mark.django_db
class TestPaymentAPIViewSet:
    endpoint_payment_gateways = reverse('payment_set-gates')
    endpoint_create_payment_order = reverse('payment_set-create_order')

    @pytest.mark.skip('Constantly changing, not relevant for the test')
    def test_get_payment_gateways(self, api_client, get_api_client):
        response_usd = api_client.get(self.endpoint_payment_gateways).json()
        assert response_usd == [{
            "id": "ivendpay",
            "label": "IvendPay",
        }, {
            "id": "paypal",
            "label": "PayPal",
        }, {
            "id": "payadmit",
            "label": "PayAdmit",
        },
            #     {
            #     "id": "stripe",
            #     "label": "Stripe",
            # }
        ]
        assert response_usd == api_client.get(self.endpoint_payment_gateways + '?currency=usd').json()

        assert api_client.get(self.endpoint_payment_gateways + '?currency=rub').json() == [{
            "id": "ivendpay",
            "label": "IvendPay"
        }]

        user = UserFactory()
        response_usd = get_api_client(user_id=user.pk).get(self.endpoint_payment_gateways).json()
        assert response_usd == [{
            "id": "ivendpay",
            "label": "IvendPay",
        }, {
            "id": "paypal",
            "label": "PayPal",
        }, {
            "id": "payadmit",
            "label": "PayAdmit",
        },
            #     {
            #     "id": "stripe",
            #     "label": "Stripe",
            # }
        ]
        assert response_usd == get_api_client(user_id=user.pk).get(
            self.endpoint_payment_gateways + '?currency=usd').json()

        assert get_api_client(user_id=user.pk).get(self.endpoint_payment_gateways + '?currency=rub').json() == [{
            "id": "ivendpay",
            "label": "IvendPay"
        }]

    def test_create_payment_order__403(self, api_client):
        response = api_client.post(self.endpoint_create_payment_order, format='json', data={
            'gateway_id': GatewayType.paypal,
            'currency': Currency.USD,
            'product_id': 1,
            'extra_data': {},
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_payment_order__incorrect_product(self, get_api_client):
        user = UserFactory()
        response = get_api_client(user_id=user.pk).post(self.endpoint_create_payment_order, format='json', data={
            'gateway_id': GatewayType.paypal,
            'currency': Currency.USD,
            'product_id': 666,
            'extra_data': {},
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert list(response.json().keys()) == ['product_id']

    def test_create_payment_order__incorrect_currency(self, get_api_client):
        user = UserFactory()

        product = ProductFactory(id=55)
        PriceFactory(pk=12312, product=product, currency=Currency.USD)
        response = get_api_client(user_id=user.pk).post(self.endpoint_create_payment_order, format='json', data={
            'gateway_id': GatewayType.paypal,
            'currency': Currency.RUB,
            'product_id': product.id,
            'extra_data': {},
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert list(response.json().keys()) == ['currency']

    @pytest.mark.skip('Legacy')
    @pytest.mark.parametrize('gateway_type, cur', [
        (GatewayType.ivendpay, Currency.USD),
        # (GatewayType.paypal, Currency.USD),
        # (GatewayType.payadmit, Currency.USD),
    ])
    def test_create_payment_order__success(self, gateway_type: GatewayType, cur: Currency, get_api_client, mocker):
        profile = ProfileFactory()

        product_obj = Product.objects.get(pk=3)
        product_price = Price.objects.get(product=product_obj)

        order = PaymentOrderFactory(
            user=profile.owner,
            product=product_obj,
            price=product_price.price,
            currency=cur,
            gateway_type=gateway_type,
        )

        class MockPaymentGate:
            @classmethod
            def create(cls, user, product, currency, **options):
                assert user == profile.owner
                assert product == product_obj
                assert currency == cur
                return order

        mocker.patch('apps.shop.rest.views.get_payment_gateway',
                     return_value=MockPaymentGate)

        response = get_api_client(user_id=profile.pk).post(self.endpoint_create_payment_order,
                                                           format='json',
                                                           data={
                                                               'gateway_id': gateway_type,
                                                               'currency': cur,
                                                               'product_id': product_obj.id,
                                                           })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': str(order.id),
            'payment_url': order.payment_url,
            'product': {
                'id': product_obj.id,
                'title': product_obj.public_title,
                'description': product_obj.public_description,
                'image': None,
                'price': '%.2f' % product_price.price,
                'currency': cur.label,
                'type': product_obj.type,
                'amount': '%.2f' % product_obj.amount,
                'lifetime': product_obj.lifetime,
                'paypal_billing_plan_id': product_price.paypal_billing_plan_id,
                'lifetime_type': 'month',
            },
            'price': '%.2f' % product_price.price,
            'currency': cur.value,
            'gateway': gateway_type.label,
            'status': 0,
            'expiry_at': order.expiry_at,
            'created': order.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'updated': order.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }


@pytest.mark.django_db
class TestCancelSubscription:
    endpoint_url = reverse('cancel_subscription')

    @pytest.mark.parametrize('product_id', (1, 2, 3, 4, 5, 6))
    def test_success_ivendpay(self, product_id: int, get_api_client):
        product = Product.objects.get(pk=product_id)
        profile = ProfileFactory()
        profile_subscription = ProfileSubscriptionFactory(profile=profile, subscription=product)
        PaymentOrderFactory(user=profile.owner, product=product, status=PaymentOrder.Status.PAID,
                            gateway_type=GatewayType.ivendpay)

        assert profile.type != ProfileType.basic

        response = get_api_client(user_id=profile.pk).post(self.endpoint_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert Profile.objects.get(pk=profile.pk).type == ProfileType.basic
        assert not ProfileSubscription.objects.get(pk=profile_subscription.pk).is_active

    @pytest.mark.parametrize('product_id', (1, 2, 3, 4, 5, 6))
    def test_success_paypal_subscription(self, product_id: int, get_api_client, mocker):
        fake_sub_id = 'FAKE-PAYPAL-ID'
        fake_auth_token = 'Bearer FAKE-PAYPAL-AUTO-TOKEN'

        product = Product.objects.get(pk=product_id)
        profile = ProfileFactory()
        profile_subscription = ProfileSubscriptionFactory(profile=profile, subscription=product)
        PaymentOrderFactory(user=profile.owner, product=product, status=PaymentOrder.Status.PAID,
                            gateway_type=GatewayType.paypal_subscription,
                            sub_id=fake_sub_id)

        assert profile.type != ProfileType.basic

        def mock_make_request(method: str, url: str, headers: dict, json: dict,
                              raise_for_status: bool, return_obj: bool):
            assert method == 'POST'
            assert url == f'https://api-m.paypal.com/v1/billing/subscriptions/{fake_sub_id}/cancel'
            assert headers == {
                'Content-Type': 'application/json',
                'Authorization': fake_auth_token
            }
            assert json == {
                'reason': 'Not satisfied with the service',
            }
            assert not raise_for_status
            assert return_obj

            class FakeResponse:
                status_code = status.HTTP_204_NO_CONTENT

            return FakeResponse

        mocker.patch(
            'apps.shop.gate.base.BaseGate.make_request',
            new=mock_make_request,
        )

        mocker.patch(
            'apps.shop.gate.paypal_subscription.PaymentGate.get_auth_token',
            return_value=fake_auth_token,
        )

        response = get_api_client(user_id=profile.pk).post(self.endpoint_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert Profile.objects.get(pk=profile.pk).type == ProfileType.basic
        assert not ProfileSubscription.objects.get(pk=profile_subscription.pk).is_active

    @pytest.mark.parametrize('product_id', (1, 2, 3, 4, 5, 6))
    def test_success_stripe(self, product_id: int, get_api_client, mocker):
        fake_sub_id = 'FAKE-STRIPE-ID'

        product = Product.objects.get(pk=product_id)
        profile = ProfileFactory()
        profile_subscription = ProfileSubscriptionFactory(profile=profile, subscription=product)
        PaymentOrderFactory(user=profile.owner, product=product, status=PaymentOrder.Status.PAID,
                            gateway_type=GatewayType.stripe,
                            sub_id=fake_sub_id)

        assert profile.type != ProfileType.basic

        def mock_stripe_subscription_cancel(idempotency_key: str, api_key: str):
            assert idempotency_key == fake_sub_id
            assert api_key == settings.STRIPE_API_KEY

        mocker.patch(
            'stripe._subscription.Subscription.cancel',
            new=mock_stripe_subscription_cancel,
        )

        response = get_api_client(user_id=profile.pk).post(self.endpoint_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert Profile.objects.get(pk=profile.pk).type == ProfileType.basic
        assert not ProfileSubscription.objects.get(pk=profile_subscription.pk).is_active

    def test_error(self, get_api_client):
        profile1 = ProfileFactory(type=ProfileType.basic)

        response = get_api_client(user_id=profile1.pk).post(self.endpoint_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

        profile2 = ProfileFactory(type=ProfileType.premium)

        response = get_api_client(user_id=profile2.pk).post(self.endpoint_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('product_id', (1, 2, 3, 4, 5, 6))
    def test_error_paypal_subscription(self, product_id: int, get_api_client, mocker):
        fake_sub_id = 'FAKE-PAYPAL-ID'
        fake_auth_token = 'Bearer FAKE-PAYPAL-AUTO-TOKEN'

        product = Product.objects.get(pk=1)
        profile = ProfileFactory()
        profile_subscription = ProfileSubscriptionFactory(profile=profile, subscription=product)
        PaymentOrderFactory(user=profile.owner, product=product, status=PaymentOrder.Status.PAID,
                            gateway_type=GatewayType.paypal_subscription,
                            sub_id=fake_sub_id)

        assert profile.type != ProfileType.basic

        def mock_make_request(method: str, url: str, headers: dict, json: dict,
                              raise_for_status: bool, return_obj: bool):
            assert method == 'POST'
            assert url == f'https://api-m.paypal.com/v1/billing/subscriptions/{fake_sub_id}/cancel'
            assert headers == {
                'Content-Type': 'application/json',
                'Authorization': fake_auth_token
            }
            assert json == {
                'reason': 'Not satisfied with the service',
            }
            assert not raise_for_status
            assert return_obj

            class FakeResponse:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return FakeResponse

        mocker.patch(
            'apps.shop.gate.base.BaseGate.make_request',
            new=mock_make_request,
        )

        mocker.patch(
            'apps.shop.gate.paypal_subscription.PaymentGate.get_auth_token',
            return_value=fake_auth_token,
        )

        response = get_api_client(user_id=profile.pk).post(self.endpoint_url)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {
            'detail': 'Error on PayPal',
        }

        assert Profile.objects.get(pk=profile.pk).type == profile.type
        assert ProfileSubscription.objects.get(pk=profile_subscription.pk).is_active

    @pytest.mark.parametrize('product_id', (1, 2, 3, 4, 5, 6))
    def test_error_stripe(self, product_id: int, get_api_client, mocker):
        fake_sub_id = 'FAKE-STRIPE-ID'

        product = Product.objects.get(pk=product_id)
        profile = ProfileFactory()
        profile_subscription = ProfileSubscriptionFactory(profile=profile, subscription=product)
        PaymentOrderFactory(user=profile.owner, product=product, status=PaymentOrder.Status.PAID,
                            gateway_type=GatewayType.stripe,
                            sub_id=fake_sub_id)

        assert profile.type != ProfileType.basic

        def mock_stripe_subscription_cancel(idempotency_key: str, api_key: str):
            assert idempotency_key == fake_sub_id
            assert api_key == settings.STRIPE_API_KEY
            raise ValueError

        mocker.patch(
            'stripe._subscription.Subscription.cancel',
            new=mock_stripe_subscription_cancel,
        )

        response = get_api_client(user_id=profile.pk).post(self.endpoint_url)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {
            'detail': 'Error on Stripe',
        }

        assert Profile.objects.get(pk=profile.pk).type == profile.type
        assert ProfileSubscription.objects.get(pk=profile_subscription.pk).is_active
