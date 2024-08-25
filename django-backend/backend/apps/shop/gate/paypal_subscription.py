import json
import base64
from urllib.parse import urljoin

from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException
from rest_framework import status as status_codes

from core.users.models import User
from apps.shop.gate.base import BaseGate, log
from apps.shop.models import Product, Price, Currency, GatewayType, PaymentOrder, PaymentOrderLog

EXTERNAL_STATUSES = {
    'cancel': PaymentOrder.Status.CANCEL,
    'success': PaymentOrder.Status.PAID,
}


def get_product_info_by_plan_id(plan_id: str) -> dict:
    price = Price.objects.filter(paypal_billing_plan_id=plan_id).first()
    return {
        'id': price.product_id,
        'currency': price.currency,
    }


class PaymentGate(BaseGate):
    gateway_type = GatewayType.paypal_subscription
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
    def get_product_by_subscription_id(cls, subscription_id: str) -> tuple[Product, Currency, str]:
        response = cls.make_request(
            method='GET',
            url=urljoin(cls.endpoint_url, f'/v1/billing/subscriptions/{subscription_id}'),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': cls.get_auth_token(),
            },
        )
        data = get_product_info_by_plan_id(plan_id=response['plan_id'])
        product = Product.objects.get(pk=data['id'])
        return product, data['currency'], response['plan_id']

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
            status=PaymentOrder.Status.PAID,
            sub_id=options.pop('subscription_id'),
            invoice_id=options.pop('invoice_id'),
            extra=json.dumps(options),
            from_shop=options.get('from_shop', False),
        )
        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Full creation of an order')

        cls.after_paid(profile=user.profile, order=order)

        return order

    @classmethod
    def check_subscription_status(cls, order: PaymentOrder) -> bool:
        super().check_subscription_status(order=order)
        response = cls.make_request(
            method='GET',
            url=urljoin(cls.endpoint_url, f'/v1/billing/subscriptions/{order.sub_id}'),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': cls.get_auth_token(),
            },
            raise_for_status=False,
            return_obj=True,
        )
        if response.status_code != status_codes.HTTP_200_OK:
            return False

        response = response.json()
        status = response['status'] == 'ACTIVE'

        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text=f'Checking subscription: {status}')

        return status

    @classmethod
    @transaction.atomic()
    def cancel_subscription(cls, order: PaymentOrder):
        super().cancel_subscription(order=order)

        response = cls.make_request(
            method='POST',
            url=urljoin(cls.endpoint_url, f'/v1/billing/subscriptions/{order.sub_id}/cancel'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': cls.get_auth_token(),
            },
            json={
                'reason': _('Not satisfied with the service'),
            },
            raise_for_status=False,
            return_obj=True,
        )

        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Disable subscription')

        if response.status_code != status_codes.HTTP_204_NO_CONTENT:
            raise APIException({
                'detail': _('Error on PayPal')
            })
