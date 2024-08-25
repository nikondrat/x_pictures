import base64
import json
from urllib.parse import urljoin
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from core.users.models import User
from apps.profiles.models import Profile
from apps.shop.gate.base import BaseGate, log
from apps.shop.models import Product, Currency, GatewayType, PaymentOrder, PaymentOrderLog

EXTERNAL_STATUSES = {
    'cancel': PaymentOrder.Status.CANCEL,
    'success': PaymentOrder.Status.PAID,
}


class PaymentGate(BaseGate):
    gateway_type = GatewayType.paypal
    endpoint_url = 'https://api-m.paypal.com/'

    if hasattr(settings, 'NGROK_DOMAIN'):
        domain = settings.NGROK_DOMAIN
    else:
        domain = settings.SHOP_DOMAIN

    @classmethod
    def get_auth_token(cls) -> str:
        token = base64.b64encode((settings.PAYPAL_CLIENT_ID + ":" + settings.PAYPAL_SECRET_KEY).encode())
        response = cls.make_request(
            method='POST',
            url=urljoin(cls.endpoint_url, '/v1/oauth2/token'),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {token.decode()}',
            },
            data={
                'grant_type': 'client_credentials',
            }
        )
        return f'Bearer {response["access_token"]}'

    @classmethod
    @transaction.atomic()
    def create(cls, user: User, product: Product, currency: Currency, **options) -> PaymentOrder:
        price = product.get_price_by_currency(currency=currency)

        order = cls.model.objects.create(
            user=user,
            gateway_type=cls.gateway_type,
            product=product,
            price=price,
            currency=currency,
            from_shop=options.get('from_shop', False),
        )

        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Creating an order object')

        landing_page = 'GUEST_CHECKOUT' if options.get('action') == 'debit_or_credit_card' else 'LOGIN'

        response = cls.make_request(
            method='POST',
            url=urljoin(cls.endpoint_url, '/v2/checkout/orders'),
            headers={
                'Content-Type': 'application/json',
                'PayPal-Request-Id': str(order.pk),
                'Authorization': cls.get_auth_token(),
            },
            json={
                'intent': 'CAPTURE',
                'purchase_units': [{
                    'reference_id': product.pk,
                    'description': product.public_description,
                    'amount': {
                        'currency_code': currency.value.upper(),
                        'value': '%.2f' % price,
                    },
                }],
                'payment_source': {
                    'paypal': {
                        'experience_context': {
                            'payment_method_preference': 'IMMEDIATE_PAYMENT_REQUIRED',
                            'brand_name': 'X Pictures',
                            'locale': 'en-US',
                            'landing_page': landing_page,
                            'shipping_preference': 'NO_SHIPPING',
                            'user_action': 'PAY_NOW',
                            'return_url': urljoin(cls.domain, reverse('paypal_callback')) + '?action=success',
                            'cancel_url': urljoin(cls.domain, reverse('paypal_callback')) + '?action=cancel',
                        }
                    }
                }
            },
        )

        order.invoice_id = response['id']
        order.payment_url = response['links'][1]['href']
        order.expiry_at = timezone.now() + timedelta(hours=3)
        order.extra = json.dumps({
            'landing_page': landing_page,
        })
        order.save()
        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Full creation of an order')

        return order

    @classmethod
    @transaction.atomic()
    def after_paid(cls, profile: Profile, order: PaymentOrder):
        # Confirm payment
        cls.make_request(
            method='POST',
            url=urljoin(cls.endpoint_url, f'/v2/checkout/orders/{order.invoice_id}/capture'),
            headers={
                'Content-Type': 'application/json',
                'PayPal-Request-Id': str(order.pk),
                'Authorization': cls.get_auth_token(),
            },
        )
        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Capture checkout payment')
        super().after_paid(profile=profile, order=order)
