import time
import uuid
import json
from urllib.parse import urljoin
from datetime import datetime, timedelta

import pytest

from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.test import override_settings
from rest_framework import status, exceptions

from apps.shop.gate import get_payment_gateway

from core.users.factories import UserFactory, AlanBaseFactory
from apps.profiles.models import ProfileType, Profile, ProfileSubscription
from apps.profiles.factories import ProfileFactory
from apps.shop.models import Currency, ProductType, GatewayType, Product, Price, PaymentOrder, StripeCustomer
from apps.shop.factories import ProductFactory, PriceFactory, PaymentOrderFactory

FAKE_FRONT_SHOP_DOMAIN = 'https://fake-shop-front-domain.com/'
FAKE_SHOP_DOMAIN = 'https://fake-shop-domain.com/'


@pytest.mark.django_db
@pytest.mark.parametrize('gateway_type, sub_id6, sub_id5', [
    (GatewayType.ivendpay, 'IvendPay', None),
    (GatewayType.paypal, 'PayPal', 'test'),
    (GatewayType.paypal_subscription, 'PayPal', None),
    (GatewayType.patreon, 'Patreon', 'test2'),
    (GatewayType.payadmit, 'PayAdmit', None),
])
def test_conversion_callback_with_click_id(gateway_type: GatewayType, sub_id6: str, sub_id5: str, mocker):
    from apps.shop.gate.base import _conversion_callback

    product = Product.objects.get(pk=1)
    user = UserFactory()
    alanbase = AlanBaseFactory(user=user, sub_id5=sub_id5)

    crypto_currency = 'usdt'
    crypto_amount = '%.2f' % product.get_price_by_currency(currency=Currency.USD)

    order = PaymentOrderFactory(status=PaymentOrder.Status.PAID,
                                gateway_type=gateway_type,
                                user=user,
                                price=product.get_price_by_currency(currency=Currency.USD),
                                currency=Currency.USD,
                                product=product,
                                extra=json.dumps({
                                    'crypto_currency': crypto_currency,
                                    'crypto_amount': crypto_amount,
                                }))

    def mock_make_payment(click_id: str, amount: float, payment_id: str, **extra):
        assert click_id == alanbase.click_id
        assert amount == float(order.price)
        assert payment_id == str(order.pk)
        assert extra['sub_id6'] == sub_id6
        if sub_id5:
            assert extra['sub_id5'] == sub_id5

    mocker.patch(
        'apps.shop.gate.base.alanbase_client.make_payment',
        new=mock_make_payment
    )
    _conversion_callback(order)


@pytest.mark.django_db
@pytest.mark.parametrize('gateway_type, sub_id6, sub_id5', [
    (GatewayType.ivendpay, 'IvendPay', None),
    (GatewayType.paypal, 'PayPal', 'test'),
    (GatewayType.paypal_subscription, 'PayPal', None),
    (GatewayType.patreon, 'Patreon', 'test2'),
    (GatewayType.payadmit, 'PayAdmit', None),
])
def test_conversion_callback_without_click_id(gateway_type: GatewayType, sub_id6: str, sub_id5: str, mocker):
    from apps.shop.gate.base import _conversion_callback

    product = Product.objects.get(pk=1)
    user = UserFactory()
    AlanBaseFactory(click_id=None, user=user, sub_id5=sub_id5)

    crypto_currency = 'usdt'
    crypto_amount = '%.2f' % product.get_price_by_currency(currency=Currency.USD)

    order = PaymentOrderFactory(status=PaymentOrder.Status.PAID,
                                gateway_type=gateway_type,
                                user=user,
                                price=product.get_price_by_currency(currency=Currency.USD),
                                currency=Currency.USD,
                                product=product,
                                extra=json.dumps({
                                    'crypto_currency': crypto_currency,
                                    'crypto_amount': crypto_amount,
                                }))

    def mock_make_payment_without_click_id(user_id: str, amount: float, payment_id: str, **extra):
        assert user_id == user.pk
        assert amount == float(order.price)
        assert payment_id == str(order.pk)
        assert extra['sub_id6'] == sub_id6
        if sub_id5:
            assert extra['sub_id5'] == sub_id5

    mocker.patch(
        'apps.shop.gate.base.alanbase_client.make_payment_without_click_id',
        new=mock_make_payment_without_click_id
    )
    _conversion_callback(order)


@pytest.mark.django_db
@pytest.mark.skip('Not used')
@override_settings(FRONT_SHOP_DOMAIN=FAKE_FRONT_SHOP_DOMAIN)
@override_settings(SHOP_DOMAIN=FAKE_SHOP_DOMAIN)
def test_redirect_url():
    from apps.shop.gate.base import BaseGate
    product = Product.objects.get(pk=1)

    order_book_success = PaymentOrderFactory(status=PaymentOrder.Status.PAID, from_shop=True, product=product)

    success_url = BaseGate.render_success_redirect_url(order_book_success)
    assert success_url == urljoin(FAKE_FRONT_SHOP_DOMAIN, '/?payment=success')
    assert BaseGate.render_redirect_url(order=order_book_success) == success_url

    order_book_cancel = PaymentOrderFactory(status=PaymentOrder.Status.CANCEL, from_shop=True, product=product)
    cancel_url = BaseGate.render_cancel_redirect_url(order_book_cancel)
    assert cancel_url == FAKE_FRONT_SHOP_DOMAIN
    assert BaseGate.render_redirect_url(order=order_book_cancel) == cancel_url

    order_success = PaymentOrderFactory(status=PaymentOrder.Status.PAID, from_shop=False, product=product)
    success_url = BaseGate.render_success_redirect_url(order_success)
    next_payment = (timezone.now() + timedelta(seconds=order_success.product.lifetime)).strftime('%d.%m.%Y')
    assert success_url == urljoin(FAKE_FRONT_SHOP_DOMAIN,
                                  f'/checkout-redirect/?payment=success&next_payment={next_payment}')
    assert BaseGate.render_redirect_url(order=order_success) == success_url

    order_cancel = PaymentOrderFactory(status=PaymentOrder.Status.CANCEL, from_shop=False, product=product)
    cancel_url = BaseGate.render_cancel_redirect_url(order_cancel)
    assert cancel_url == urljoin(FAKE_FRONT_SHOP_DOMAIN, '/checkout-redirect/?payment=cancel')
    assert BaseGate.render_redirect_url(order=order_cancel) == cancel_url


class BaseTestPaymentGate:
    gateway_type: GatewayType

    @pytest.fixture(autouse=True)
    def setup(self):
        self.profile = ProfileFactory()
        self.product = ProductFactory(id=33, subscription=True)
        self.product_price_usd = PriceFactory(id=66, product=self.product, currency=Currency.USD)
        self.product_price_rub = PriceFactory(id=89, product=self.product, currency=Currency.RUB)
        self.gate = get_payment_gateway(gateway_type=self.gateway_type)


@pytest.mark.django_db
class TestIvendPayPaymentGate(BaseTestPaymentGate):
    gateway_type = GatewayType.ivendpay

    @pytest.mark.parametrize('currency', [
        Currency.USD,
        Currency.RUB
    ])
    def test_create__error_validate_options(self, currency: Currency):
        with pytest.raises(exceptions.ValidationError) as err_info:
            self.gate.create(
                user=self.profile.owner,
                product=self.product,
                currency=currency,
            )
            assert err_info.value == {'extra_data': {
                'crypto_currency': 'No cryptocurrency is specified'
            }}

    @pytest.mark.parametrize('currency', [
        Currency.USD,
        Currency.RUB
    ])
    def test_create__success(self, currency: Currency, mocker, faker):
        crypto_currency = 'usdt'
        crypto_amount = '%.2f' % self.product.get_price_by_currency(currency=currency)
        fake_invoice_id = str(uuid.uuid4().hex)
        fake_payment_url = faker.unique.url()
        fake_expiry_at = int(time.time())

        def mock_low_make_request(method: str, url: str, headers=None, **options):
            assert method == 'POST'
            assert url == urljoin(self.gate.endpoint_url, '/api/v3/create')
            assert headers == {
                'X-API-KEY': settings.IVENDPAY_API_KEY,
            }
            assert options.get('json') == {
                'currency': crypto_currency,
                'amount_fiat': '%.2f' % self.product.get_price_by_currency(currency=currency),
                'currency_fiat': currency.value.upper()
            }
            return {'data': [{
                'invoice': fake_invoice_id,
                'payment_url': fake_payment_url,
                'currency': crypto_currency,
                'amount': crypto_amount,
                'expiry_at': fake_expiry_at,
            }]}

        mocker.patch(
            'apps.shop.gate.ivendpay.BaseGate._make_request',
            new=mock_low_make_request
        )

        order = self.gate.create(
            user=self.profile.owner,
            product=self.product,
            currency=currency,
            crypto_currency=crypto_currency,
        )

        assert order.invoice_id == fake_invoice_id
        assert order.payment_url == fake_payment_url
        assert order.user == self.profile.owner
        assert order.gateway_type == self.gate.gateway_type
        assert order.product == self.product
        assert order.price == self.product.get_price_by_currency(currency=currency)
        assert order.currency == currency
        assert json.loads(order.extra) == {
            'crypto_currency': crypto_currency,
            'crypto_amount': crypto_amount,
        }
        assert order.expiry_at == timezone.make_aware(datetime.fromtimestamp(fake_expiry_at))

    def test_update__permission_error(self, api_client):
        response = api_client.post(reverse('ivendpay_webhook'))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('product_id, profile_type', [
        (1, ProfileType.advance),
        (4, ProfileType.premium),
        (5, ProfileType.super_premium),
    ])
    @pytest.mark.parametrize('external_status, tx_hash, explorer_url, result_status', [
        ('CANCELED', '-', '-', PaymentOrder.Status.CANCEL),
        ('TIMEOUT', '-', '-', PaymentOrder.Status.CANCEL),
        ('PAID', 'https://fake-tx_hash/', 'https://fake-explorer_url/', PaymentOrder.Status.PAID),
        ('ERROR', None, None, PaymentOrder.Status.ERROR),
    ])
    def test_update__subscription(self, external_status: str, tx_hash: str, explorer_url: str,
                                  result_status: PaymentOrder.Status, product_id: int, profile_type: ProfileType,
                                  api_client, mocker):
        product = Product.objects.get(pk=product_id)
        profile = ProfileFactory(type=ProfileType.basic, balance=0)
        crypto_currency = 'usdt'
        crypto_amount = '%.2f' % product.get_price_by_currency(currency=Currency.USD)

        order = PaymentOrderFactory(status=PaymentOrder.Status.CREATED,
                                    gateway_type=GatewayType.ivendpay,
                                    user=profile.owner,
                                    price=product.get_price_by_currency(currency=Currency.USD),
                                    currency=Currency.USD,
                                    product=product,
                                    extra=json.dumps({
                                        'crypto_currency': crypto_currency,
                                        'crypto_amount': crypto_amount,
                                    }))

        mocker.patch(
            'apps.shop.gate.base._conversion_callback',
            return_value=None,
        )
        mocker.patch(
            'apps.shop.gate.base._after_paid_call_tasks',
            return_value=None,
        )

        payment_data = {
            'payment_status': external_status,
            'invoice': order.invoice_id,
            'hash': tx_hash,
            'explorer_url': explorer_url,
        }

        api_client.credentials(
            HTTP_X_API_KEY=settings.IVENDPAY_API_KEY,
        )
        response = api_client.post(
            reverse('ivendpay_webhook'),
            data={
                json.dumps(payment_data): ''
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_order = PaymentOrder.objects.get(pk=order.pk)
        assert updated_order.status == result_status
        assert json.loads(updated_order.extra) == {
            'crypto_currency': crypto_currency,
            'crypto_amount': crypto_amount,
            'transaction_hash': tx_hash,
            'explorer_url': explorer_url,
        }

        updated_profile = Profile.objects.get(pk=profile.pk)

        if updated_order.is_paid:
            assert updated_profile.type == profile_type
            assert updated_profile.balance == product.amount
            profile_subscription = ProfileSubscription.objects.filter(profile=profile,
                                                                      is_active=True).first()

            assert profile_subscription.subscription == product

    @pytest.mark.parametrize('external_status, tx_hash, explorer_url, result_status', [
        ('CANCELED', '-', '-', PaymentOrder.Status.CANCEL),
        ('TIMEOUT', '-', '-', PaymentOrder.Status.CANCEL),
        ('PAID', 'https://fake-tx_hash/', 'https://fake-explorer_url/', PaymentOrder.Status.PAID),
        ('ERROR', None, None, PaymentOrder.Status.ERROR),
    ])
    def test_update__one_time(self, external_status: str, tx_hash: str, explorer_url: str,
                              result_status: PaymentOrder.Status, api_client, mocker):
        product = ProductFactory(pk=555, type=ProductType.one_time, amount=150)
        PriceFactory(pk=777, product=product, currency=Currency.USD)
        profile = ProfileFactory(type=ProfileType.basic, balance=0)
        crypto_currency = 'usdt'
        crypto_amount = '%.2f' % product.get_price_by_currency(currency=Currency.USD)

        order = PaymentOrderFactory(status=PaymentOrder.Status.CREATED,
                                    gateway_type=GatewayType.ivendpay,
                                    user=profile.owner,
                                    price=product.get_price_by_currency(currency=Currency.USD),
                                    currency=Currency.USD,
                                    product=product,
                                    extra=json.dumps({
                                        'crypto_currency': crypto_currency,
                                        'crypto_amount': crypto_amount,
                                    }))

        mocker.patch(
            'apps.shop.gate.base._conversion_callback',
            return_value=None,
        )
        mocker.patch(
            'apps.shop.gate.base._after_paid_call_tasks',
            return_value=None,
        )

        payment_data = {
            'payment_status': external_status,
            'invoice': order.invoice_id,
            'hash': tx_hash,
            'explorer_url': explorer_url,
        }

        api_client.credentials(
            HTTP_X_API_KEY=settings.IVENDPAY_API_KEY,
        )
        response = api_client.post(
            reverse('ivendpay_webhook'),
            data={
                json.dumps(payment_data): ''
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_order = PaymentOrder.objects.get(pk=order.pk)
        assert updated_order.status == result_status
        assert json.loads(updated_order.extra) == {
            'crypto_currency': crypto_currency,
            'crypto_amount': crypto_amount,
            'transaction_hash': tx_hash,
            'explorer_url': explorer_url,
        }

        updated_profile = Profile.objects.get(pk=profile.pk)

        if updated_order.is_paid:
            assert updated_profile.type == ProfileType.basic
            assert updated_profile.balance == product.amount
            assert not ProfileSubscription.objects.filter(profile=profile).exists()


@pytest.mark.django_db
class TestPayAdmitPaymentGate(BaseTestPaymentGate):
    gateway_type = GatewayType.payadmit

    @pytest.mark.parametrize('currency', [
        Currency.USD,
        Currency.RUB
    ])
    def test_create__success(self, currency: Currency, mocker, faker):
        fake_invoice_id = str(uuid.uuid4().hex)
        fake_payment_url = faker.unique.url()

        success_return_url = urljoin(settings.FRONT_DOMAIN,
                                     '?payment=success&next_payment={next_payment}'.format(
                                         next_payment=(timezone.now() + timedelta(
                                             seconds=self.product.lifetime)).strftime('%d.%m.%Y')
                                     ))
        cancel_return_url = urljoin(settings.FRONT_DOMAIN, '?payment=cancel')

        def mock_make_request(method: str, url: str, headers=None, **options):
            assert method == 'POST'
            assert url == urljoin(self.gate.endpoint_url, '/api/v1/payments')
            assert headers == {
                'Authorization': f'Bearer {settings.PAYADMIT_SECRET_KEY}',
            }
            options.get('json').pop('referenceId')
            assert options.get('json') == {
                'paymentType': 'DEPOSIT',
                'paymentMethod': 'BASIC_CARD',
                'amount': float(self.product.get_price_by_currency(currency=currency)),
                'currency': currency.value.upper(),
                'description': self.product.public_description,
                'customer': {
                    'referenceId': self.profile.pk,
                    'email': self.profile.owner.email,
                },
                'returnUrl': cancel_return_url,
                'successReturnUrl': success_return_url,
                'declineReturnUrl': cancel_return_url,
                'webhookUrl': urljoin(self.gate.domain, reverse('payadmit_webhook')),
            }
            return {
                'status': 200,
                'result': {
                    'id': fake_invoice_id,
                    'redirectUrl': fake_payment_url,
                    'paymentMethod': 'BASIC_CARD'
                }
            }

        mocker.patch(
            'apps.shop.gate.payadmit.BaseGate.make_request',
            new=mock_make_request
        )

        order = self.gate.create(
            user=self.profile.owner,
            product=self.product,
            currency=currency,
            payment_method='BASIC_CARD',
        )

        assert order.invoice_id == fake_invoice_id
        assert order.payment_url == fake_payment_url
        assert order.user == self.profile.owner
        assert order.gateway_type == self.gate.gateway_type
        assert order.product == self.product
        assert order.price == self.product.get_price_by_currency(currency=currency)
        assert order.currency == currency
        assert json.loads(order.extra) == {
            'payment_method': 'BASIC_CARD',
        }

    def test_update__permission_error(self, api_client):
        response = api_client.post(reverse('payadmit_webhook'))
        assert response.status_code == status.HTTP_403_FORBIDDEN

        api_client.credentials(HTTP_SIGNATURE='gasdgasdgfasdgasdgasdg241241241', )
        response = api_client.post(reverse('payadmit_webhook'),
                                   data={
                                       'id': str(uuid.uuid4()),
                                   })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('product_id, profile_type', [
        (1, ProfileType.advance),
        (4, ProfileType.premium),
        (5, ProfileType.super_premium),
    ])
    @pytest.mark.parametrize('external_status, result_status', [
        ('CANCELLED', PaymentOrder.Status.CANCEL),
        ('DECLINED', PaymentOrder.Status.CANCEL),
        ('COMPLETED', PaymentOrder.Status.PAID),
        ('ERROR', PaymentOrder.Status.ERROR),
    ])
    def test_update__subscription(self, external_status: str, result_status: PaymentOrder.Status,
                                  product_id: int, profile_type: ProfileType,
                                  api_client, mocker):
        product = Product.objects.get(pk=product_id)
        profile = ProfileFactory(type=ProfileType.basic, balance=0)

        order = PaymentOrderFactory(status=PaymentOrder.Status.CREATED,
                                    gateway_type=GatewayType.payadmit,
                                    user=profile.owner,
                                    price=product.get_price_by_currency(currency=Currency.USD),
                                    currency=Currency.USD,
                                    product=product,
                                    extra=json.dumps({
                                        'payment_method': 'BASIC_CARD',
                                    }))

        mocker.patch(
            'apps.shop.gate.base._conversion_callback',
            return_value=None,
        )
        mocker.patch(
            'apps.shop.gate.base._after_paid_call_tasks',
            return_value=None,
        )
        mocker.patch(
            'apps.shop.rest.webhooks.PayAdmitSignaturePermission.has_permission',
            return_value=True,
        )

        payment_data = {
            'id': order.invoice_id,
            'state': external_status,
        }

        response = api_client.post(
            reverse('payadmit_webhook'),
            data=payment_data,
        )

        assert response.status_code == status.HTTP_200_OK

        updated_order = PaymentOrder.objects.get(pk=order.pk)
        assert updated_order.status == result_status
        assert json.loads(updated_order.extra) == {
            'payment_method': 'BASIC_CARD',
            'amount': None,
            'currency': None,
        }

        updated_profile = Profile.objects.get(pk=profile.pk)

        if updated_order.is_paid:
            assert updated_profile.type == profile_type
            assert updated_profile.balance == product.amount
            profile_subscription = ProfileSubscription.objects.filter(profile=profile,
                                                                      is_active=True).first()

            assert profile_subscription.subscription == product

    @pytest.mark.parametrize('external_status, result_status', [
        ('CANCELLED', PaymentOrder.Status.CANCEL),
        ('DECLINED', PaymentOrder.Status.CANCEL),
        ('COMPLETED', PaymentOrder.Status.PAID),
        ('ERROR', PaymentOrder.Status.ERROR),
    ])
    def test_update__one_time(self, external_status: str, result_status: PaymentOrder.Status, api_client, mocker):
        product = ProductFactory(pk=555, type=ProductType.one_time, amount=150)
        PriceFactory(pk=125, product=product, currency=Currency.USD)
        profile = ProfileFactory(type=ProfileType.basic, balance=0)

        order = PaymentOrderFactory(status=PaymentOrder.Status.CREATED,
                                    gateway_type=GatewayType.payadmit,
                                    user=profile.owner,
                                    price=product.get_price_by_currency(currency=Currency.USD),
                                    currency=Currency.USD,
                                    product=product,
                                    extra=json.dumps({
                                        'payment_method': 'BASIC_CARD',
                                    }))

        mocker.patch(
            'apps.shop.gate.base._conversion_callback',
            return_value=None,
        )
        mocker.patch(
            'apps.shop.gate.base._after_paid_call_tasks',
            return_value=None,
        )
        mocker.patch(
            'apps.shop.rest.webhooks.PayAdmitSignaturePermission.has_permission',
            return_value=True,
        )

        payment_data = {
            'id': order.invoice_id,
            'state': external_status,
        }

        response = api_client.post(
            reverse('payadmit_webhook'),
            data=payment_data,
        )

        assert response.status_code == status.HTTP_200_OK

        updated_order = PaymentOrder.objects.get(pk=order.pk)
        assert updated_order.status == result_status
        assert json.loads(updated_order.extra) == {
            'payment_method': 'BASIC_CARD',
            'amount': None,
            'currency': None,
        }

        updated_profile = Profile.objects.get(pk=profile.pk)

        if updated_order.is_paid:
            assert updated_profile.type == ProfileType.basic
            assert updated_profile.balance == product.amount
            assert not ProfileSubscription.objects.filter(profile=profile).exists()


@pytest.mark.django_db
class TestPaypalPaymentGate(BaseTestPaymentGate):
    gateway_type = GatewayType.paypal

    def test_get_auth_token(self, mocker):
        import base64
        token = base64.b64encode((settings.PAYPAL_CLIENT_ID + ":" + settings.PAYPAL_SECRET_KEY).encode())

        fake_token = 'fake-token'
        fake_bearer_token = f'Bearer {fake_token}'

        def mock_make_request(method: str, url: str, headers=None, **options):
            assert method == 'POST'
            assert url == urljoin(self.gate.endpoint_url, '/v1/oauth2/token')
            assert headers == {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {token.decode()}',
            }
            assert options.get('data') == {
                'grant_type': 'client_credentials',
            }
            return {
                'access_token': fake_token,
            }

        mocker.patch(
            'apps.shop.gate.base.BaseGate.make_request',
            new=mock_make_request,
        )

        assert self.gate.get_auth_token() == fake_bearer_token

    @pytest.mark.parametrize('currency', [
        Currency.USD,
        Currency.RUB
    ])
    def test_create__success(self, currency: Currency, mocker, faker):
        fake_invoice_id = str(uuid.uuid4().hex)
        fake_payment_url = faker.unique.url()
        fake_bearer_token = 'Bearer token'

        def mock_make_request(method: str, url: str, headers=None, **options):
            assert method == 'POST'
            assert url == urljoin(self.gate.endpoint_url, '/v2/checkout/orders')
            assert headers['Authorization'] == fake_bearer_token

            assert options.get('json') == {
                'intent': 'CAPTURE',
                'purchase_units': [{
                    'reference_id': self.product.pk,
                    'description': self.product.public_description,
                    'amount': {
                        'currency_code': currency.value.upper(),
                        'value': '%.2f' % self.product.get_price_by_currency(currency=currency),
                    },
                }],
                'payment_source': {
                    'paypal': {
                        'experience_context': {
                            'payment_method_preference': 'IMMEDIATE_PAYMENT_REQUIRED',
                            'brand_name': 'X Pictures',
                            'locale': 'en-US',
                            'landing_page': 'GUEST_CHECKOUT',
                            'shipping_preference': 'NO_SHIPPING',
                            'user_action': 'PAY_NOW',
                            'return_url': urljoin(self.gate.domain, reverse('paypal_callback')) + '?action=success',
                            'cancel_url': urljoin(self.gate.domain, reverse('paypal_callback')) + '?action=cancel',
                        }
                    }
                }
            }

            return {
                'id': fake_invoice_id,
                'links': [{}, {'href': fake_payment_url}],
            }

        mocker.patch(
            'apps.shop.gate.payadmit.BaseGate.make_request',
            new=mock_make_request
        )
        mocker.patch(
            'apps.shop.gate.paypal.PaymentGate.get_auth_token',
            return_value=fake_bearer_token,
        )

        order = self.gate.create(
            user=self.profile.owner,
            product=self.product,
            currency=currency,
            action='debit_or_credit_card',
        )

        assert order.invoice_id == fake_invoice_id
        assert order.payment_url == fake_payment_url
        assert order.user == self.profile.owner
        assert order.gateway_type == self.gate.gateway_type
        assert order.product == self.product
        assert order.price == self.product.get_price_by_currency(currency=currency)
        assert order.currency == currency
        assert json.loads(order.extra) == {
            'landing_page': 'GUEST_CHECKOUT',
        }

    @pytest.mark.parametrize('product_id, profile_type', [
        (1, ProfileType.advance),
        (4, ProfileType.premium),
        (5, ProfileType.super_premium),
    ])
    @pytest.mark.parametrize('external_status, result_status', [
        ('cancel', PaymentOrder.Status.CANCEL),
        ('success', PaymentOrder.Status.PAID),
    ])
    def test_update__subscription(self, external_status: str, result_status: PaymentOrder.Status,
                                  product_id: int, profile_type: ProfileType,
                                  api_client, mocker):
        product = Product.objects.get(pk=product_id)
        profile = ProfileFactory(type=ProfileType.basic, balance=0)

        fake_bearer_token = 'Bearer token'

        order = PaymentOrderFactory(status=PaymentOrder.Status.CREATED,
                                    gateway_type=GatewayType.paypal,
                                    user=profile.owner,
                                    price=product.get_price_by_currency(currency=Currency.USD),
                                    currency=Currency.USD,
                                    product=product,
                                    extra=json.dumps({
                                        'landing_page': 'GUEST_CHECKOUT',
                                    }))

        mocker.patch(
            'apps.shop.gate.base._conversion_callback',
            return_value=None,
        )
        mocker.patch(
            'apps.shop.gate.base._after_paid_call_tasks',
            return_value=None,
        )

        def mock_make_request(method: str, url: str, headers=None, **options):
            assert method == 'POST'
            assert urljoin(self.gate.endpoint_url, f'/v2/checkout/orders/{order.invoice_id}/capture')
            assert headers == {
                'Content-Type': 'application/json',
                'PayPal-Request-Id': str(order.pk),
                'Authorization': fake_bearer_token,
            }

        mocker.patch(
            'apps.shop.gate.paypal.PaymentGate.get_auth_token',
            return_value=fake_bearer_token,
        )
        mocker.patch(
            'apps.shop.gate.base.BaseGate.make_request',
            new=mock_make_request,
        )

        response = api_client.get(
            reverse('paypal_callback') + f'?action={external_status}&token={order.invoice_id}',
        )
        assert response.status_code == status.HTTP_302_FOUND

        updated_order = PaymentOrder.objects.get(pk=order.pk)
        assert updated_order.status == result_status
        assert json.loads(updated_order.extra) == {
            'landing_page': 'GUEST_CHECKOUT',
        }

        updated_profile = Profile.objects.get(pk=profile.pk)

        if updated_order.is_paid:
            assert updated_profile.type == profile_type
            assert updated_profile.balance == product.amount
            profile_subscription = ProfileSubscription.objects.filter(profile=profile,
                                                                      is_active=True).first()

            assert profile_subscription.subscription == product

    @pytest.mark.parametrize('external_status, result_status', [
        ('cancel', PaymentOrder.Status.CANCEL),
        ('success', PaymentOrder.Status.PAID),
    ])
    def test_update__one_time(self, external_status: str, result_status: PaymentOrder.Status, api_client, mocker):
        product = ProductFactory(pk=555, type=ProductType.one_time, amount=150)
        PriceFactory(pk=1244, product=product, currency=Currency.USD)
        profile = ProfileFactory(type=ProfileType.basic, balance=0)
        fake_bearer_token = 'Bearer token'

        order = PaymentOrderFactory(status=PaymentOrder.Status.CREATED,
                                    gateway_type=GatewayType.paypal,
                                    user=profile.owner,
                                    price=product.get_price_by_currency(currency=Currency.USD),
                                    currency=Currency.USD,
                                    product=product,
                                    extra=json.dumps({
                                        'landing_page': 'GUEST_CHECKOUT',
                                    }))

        mocker.patch(
            'apps.shop.gate.base._conversion_callback',
            return_value=None,
        )
        mocker.patch(
            'apps.shop.gate.base._after_paid_call_tasks',
            return_value=None,
        )

        def mock_make_request(method: str, url: str, headers=None, **options):
            assert method == 'POST'
            assert url == urljoin(self.gate.endpoint_url, f'/v2/checkout/orders/{order.invoice_id}/capture')
            assert headers == {
                'Content-Type': 'application/json',
                'PayPal-Request-Id': str(order.pk),
                'Authorization': fake_bearer_token,
            }

        mocker.patch(
            'apps.shop.gate.paypal.PaymentGate.get_auth_token',
            return_value=fake_bearer_token,
        )
        mocker.patch(
            'apps.shop.gate.base.BaseGate.make_request',
            new=mock_make_request,
        )

        response = api_client.get(
            reverse('paypal_callback') + f'?action={external_status}&token={order.invoice_id}',
        )
        assert response.status_code == status.HTTP_302_FOUND

        updated_order = PaymentOrder.objects.get(pk=order.pk)
        assert updated_order.status == result_status
        assert json.loads(updated_order.extra) == {
            'landing_page': 'GUEST_CHECKOUT',
        }

        updated_profile = Profile.objects.get(pk=profile.pk)

        if updated_order.is_paid:
            assert updated_profile.type == ProfileType.basic
            assert updated_profile.balance == product.amount
            assert not ProfileSubscription.objects.filter(profile=profile).exists()


@pytest.mark.django_db
class TestPaypalSubscriptionPaymentGate(BaseTestPaymentGate):
    gateway_type = GatewayType.paypal_subscription

    @pytest.mark.parametrize('plan_id, product_id, currency', [
        ('P-9SK84495DC4552244MVPAASY', 5, Currency.USD),  # Super premium
        ('P-34L125305N328910KMVO77SY', 3, Currency.USD),  # Premium Month
    ])
    def test_get_product_by_subscription_id(self, plan_id: str, product_id: int, currency: Currency, mocker):

        fake_subscription_id = '2412512351235'

        def mock_make_request(method: str, url: str, headers=None, **options):
            assert method == 'GET'
            assert url == urljoin(self.gate.endpoint_url, f'/v1/billing/subscriptions/{fake_subscription_id}')
            return {'plan_id': plan_id}

        mocker.patch(
            'apps.shop.gate.base.BaseGate.make_request',
            new=mock_make_request
        )

        mocker.patch(
            'apps.shop.gate.paypal_subscription.PaymentGate.get_auth_token',
            return_value='token'
        )

        product, cur, p_id = self.gate.get_product_by_subscription_id(fake_subscription_id)

        assert product.id == product_id
        assert cur == currency
        assert p_id == plan_id

    @pytest.mark.parametrize('product_id, profile_type', [
        (3, ProfileType.premium),
        (5, ProfileType.super_premium),
    ])
    def test_create(self, product_id: int, profile_type: ProfileType, get_api_client, mocker):
        mocker.patch(
            'apps.shop.gate.base._conversion_callback',
            return_value=None,
        )
        mocker.patch(
            'apps.shop.gate.base._after_paid_call_tasks',
            return_value=None,
        )

        def mock_make_request(method: str, url: str, headers=None, **options):
            assert method == 'GET'
            assert url == urljoin(self.gate.endpoint_url, f'/v1/billing/subscriptions/{fake_subscription_id}')
            if product_id == 3:
                return {'plan_id': 'P-34L125305N328910KMVO77SY'}
            elif product_id == 5:
                return {'plan_id': 'P-9SK84495DC4552244MVPAASY'}
            else:
                raise AssertionError('Plan ID not found')

        mocker.patch(
            'apps.shop.gate.base.BaseGate.make_request',
            new=mock_make_request
        )
        mocker.patch(
            'apps.shop.gate.paypal_subscription.PaymentGate.get_auth_token',
            return_value='fake-token'
        )

        product = Product.objects.get(pk=product_id)
        profile = ProfileFactory(type=ProfileType.basic, balance=0)
        fake_invoice_id = str(uuid.uuid4().hex)
        fake_subscription_id = '124124'

        response = get_api_client(user_id=profile.pk).post(
            reverse('paypal_subscription_callback'),
            data={
                'invoice_id': fake_invoice_id,
                'subscription_id': fake_subscription_id,
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        order = PaymentOrder.objects.get(invoice_id=fake_invoice_id)

        assert order.sub_id == fake_subscription_id
        assert order.user == profile.owner
        assert order.product.id == product_id
        assert order.currency == Currency.USD
        assert order.status == PaymentOrder.Status.PAID
        assert list(json.loads(order.extra).keys()) == ['plan_id']

        updated_profile = Profile.objects.get(pk=profile.pk)
        assert updated_profile.type == profile_type
        assert updated_profile.balance == product.amount
        profile_subscription = ProfileSubscription.objects.filter(profile=profile).first()

        assert profile_subscription.subscription_id == product_id
        assert profile_subscription.is_active

    @pytest.mark.parametrize('response_status, code, result', [
        ('ACTIVE', 200, True),
        (None, 404, False),
    ])
    def test_check_subscription_status(self, response_status: str, code: int, result: bool, mocker):
        fake_sub_id = str(uuid.uuid4())
        fake_auth_token = str(uuid.uuid4())

        order = PaymentOrderFactory(sub_id=fake_sub_id,
                                    gateway_type=self.gateway_type,
                                    status=PaymentOrder.Status.PAID,
                                    product=Product.objects.get(pk=1))

        class FakeResponse:
            status_code = code

            def json(self):
                return {'status': response_status}

        def mock_make_request(method: str, url: str, headers: dict, raise_for_status: bool,
                              return_obj: bool):
            assert method == 'GET'
            assert url == urljoin(self.gate.endpoint_url, f'/v1/billing/subscriptions/{fake_sub_id}')
            assert return_obj
            assert not raise_for_status

            assert headers == {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': fake_auth_token,
            }

            return FakeResponse()

        mocker.patch(
            'apps.shop.gate.base.BaseGate.make_request',
            new=mock_make_request
        )
        mocker.patch(
            'apps.shop.gate.paypal_subscription.PaymentGate.get_auth_token',
            return_value=fake_auth_token,
        )

        assert get_payment_gateway(gateway_type=self.gateway_type).check_subscription_status(order=order) == result


@pytest.mark.django_db
class TestStripePaymentGate(BaseTestPaymentGate):
    gateway_type = GatewayType.stripe

    def test_get_or_create_customer(self, mocker):
        fake_customer_id = 'fake-id-customer'

        user = UserFactory()

        assert not StripeCustomer.objects.all().exists()

        def mock_stripe_customer_create(api_key: str, email: str):
            assert api_key == settings.STRIPE_API_KEY
            assert email == user.email

            class FakeCustomer:
                id = fake_customer_id

            return FakeCustomer

        mocker.patch(
            'stripe._customer.Customer.create',
            new=mock_stripe_customer_create,
        )

        customer, is_created = self.gate.get_or_create_customer(user=user)
        assert customer.id == fake_customer_id
        assert is_created
        assert customer.owner == user

        assert StripeCustomer.objects.filter(owner=user).exists()

        self.gate.get_or_create_customer(user=user)

        assert StripeCustomer.objects.count() == 1

    @pytest.mark.parametrize('product_id', (1, 2, 3, 4, 5, 6))
    @pytest.mark.parametrize('currency', [
        Currency.USD,
    ])
    def test_create_subscription(self, product_id: int, currency: Currency, mocker, faker):
        usr = UserFactory()
        cst = StripeCustomer.objects.create(owner=usr, id='fake-id')

        product = Product.objects.get(pk=product_id)
        price = Price.objects.get(product=product, currency=currency)

        fake_success_checkout_token = 'fake-success-checkout-token'
        fake_cancel_checkout_token = 'fake-cancel-checkout-token'

        class FakeResponse:
            id = 'fake-id'
            url = faker.unique.url()
            expires_at = int(time.time() + 60)

        def mock_checkout_session_create(api_key: str, line_items: list[dict], mode: str,
                                         success_url: str, cancel_url: str, customer: str):
            assert api_key == settings.STRIPE_API_KEY
            assert line_items == [{
                'price': price.stripe_price_id,
                'quantity': 1,
            }]
            assert mode == 'subscription'
            base_url = urljoin(self.gate.domain, reverse('stripe_callback'))
            assert success_url == urljoin(base_url, f'?checkout_token={fake_success_checkout_token}')
            assert cancel_url == urljoin(base_url, f'?checkout_token={fake_cancel_checkout_token}')
            assert customer == cst.pk

            return FakeResponse

        mocker.patch(
            'apps.shop.gate.stripe.PaymentGate.get_or_create_customer',
            return_value=(cst, True),
        )
        mocker.patch(
            'apps.shop.gate.stripe.encode_checkout_token',
            side_effect=[fake_success_checkout_token,
                         fake_cancel_checkout_token],
        )
        mocker.patch(
            'stripe.checkout._session.Session.create',
            new=mock_checkout_session_create,
        )

        order = self.gate.create(
            user=usr,
            product=product,
            currency=currency,
        )

        assert order.invoice_id == FakeResponse.id
        assert order.price == price.price
        assert order.currency == currency
        assert order.payment_url == FakeResponse.url
        assert order.expiry_at == timezone.make_aware(datetime.fromtimestamp(FakeResponse.expires_at))

        assert json.loads(order.extra) == {
            'mode': 'subscription',
            'customer_id': cst.id,
            'stripe_price_id': price.stripe_price_id,
        }

    @pytest.mark.parametrize('product_id, profile_type', [
        (1, ProfileType.advance),
        (4, ProfileType.premium),
        (5, ProfileType.super_premium),
    ])
    @pytest.mark.parametrize('result_status', [
        PaymentOrder.Status.CANCEL,
        PaymentOrder.Status.PAID,
    ])
    def test_update_subscription(self, result_status: PaymentOrder.Status, product_id: int,
                                 profile_type: ProfileType, api_client, mocker):
        product = Product.objects.get(pk=product_id)
        profile = ProfileFactory(type=ProfileType.basic, balance=0)
        price = Price.objects.get(product=product, currency=Currency.USD)
        cst = StripeCustomer.objects.create(owner=profile.owner, id='fake-id')

        fake_checkout_token = 'fake-checkout-token'

        order = PaymentOrderFactory(status=PaymentOrder.Status.CREATED,
                                    gateway_type=GatewayType.stripe,
                                    user=profile.owner,
                                    price=product.get_price_by_currency(currency=Currency.USD),
                                    currency=Currency.USD,
                                    product=product,
                                    extra=json.dumps({
                                        'mode': 'subscription',
                                        'customer_id': cst.id,
                                        'stripe_price_id': price.stripe_price_id,
                                    }))

        class FakeResponse:
            subscription = 'fake-subscription-id'

        def mock_stripe_subscription_create(api_key: str, id: str):
            assert api_key == settings.STRIPE_API_KEY

            return FakeResponse

        mocker.patch(
            'apps.shop.gate.base._conversion_callback',
            return_value=None,
        )
        mocker.patch(
            'apps.shop.gate.base._after_paid_call_tasks',
            return_value=None,
        )
        mocker.patch(
            'stripe.checkout._session.Session.retrieve',
            new=mock_stripe_subscription_create
        )

        def mock_decode_checkout_token(checkout_token: str) -> dict:
            assert checkout_token == fake_checkout_token
            return {
                'pk': str(order.pk),
                'status': result_status.value,
            }

        mocker.patch(
            'apps.shop.gate.stripe.decode_checkout_token',
            new=mock_decode_checkout_token
        )

        response = api_client.get(reverse('stripe_callback') + f'?checkout_token={fake_checkout_token}')
        assert response.status_code == status.HTTP_302_FOUND

        updated_order = PaymentOrder.objects.get(pk=order.pk)
        assert updated_order.status == result_status

        if result_status == PaymentOrder.Status.PAID:
            assert updated_order.sub_id == FakeResponse.subscription

    @pytest.mark.parametrize('response_status, result', [
        ('active', True),
        ('inactive', False),
    ])
    def test_check_subscription_status(self, response_status: str, result: bool, mocker):
        fake_sub_id = str(uuid.uuid4())

        order = PaymentOrderFactory(sub_id=fake_sub_id,
                                    gateway_type=self.gateway_type,
                                    status=PaymentOrder.Status.PAID,
                                    product=Product.objects.get(pk=1))

        class FakeResponse:
            status = response_status

        def mock_subscription_retrieve(id: str, api_key: str):
            assert api_key == settings.STRIPE_API_KEY
            assert id == fake_sub_id
            return FakeResponse

        mocker.patch(
            'stripe._subscription.Subscription.retrieve',
            new=mock_subscription_retrieve
        )

        assert get_payment_gateway(gateway_type=self.gateway_type).check_subscription_status(order=order) == result
