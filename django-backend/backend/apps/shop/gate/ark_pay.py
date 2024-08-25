import json
import hmac
import hashlib
from datetime import timedelta
from urllib.parse import urljoin

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from core.users.models import User
from apps.shop.gate import BaseGate, log
from apps.shop.models import Product, GatewayType, Currency, PaymentOrder, PaymentOrderLog

EXTERNAL_STATUSES = {
    'COMPLETED': PaymentOrder.Status.PAID,
    'FAILED': PaymentOrder.Status.CANCEL,
}


def create_signature(method: str, uri: str, body: str, secret_key: str):
    payload = f'{method} {uri}\n{body}'
    return hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()


def check_signature(method: str, uri: str, body: str, secret_key: str, received_signature: str):
    actual_signature = create_signature(method=method,
                                        uri=uri, body=body,
                                        secret_key=secret_key)
    return actual_signature == received_signature


class PaymentGate(BaseGate):
    gateway_type = GatewayType.ark_pay
    endpoint_url = 'https://arkpay.com/'

    @classmethod
    def generate_signature(cls, payload: dict):
        return create_signature(
            method='POST',
            uri='/api/v1/merchant/api/transactions',
            # body=json.dumps(payload, separators=(",", ":")),
            body=json.dumps(payload),
            secret_key=settings.ARK_PAY_SECRET_KEY,
        )

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

        payload = {
            'merchantTransactionId': str(order.pk),
            'amount': float(price),
            'currency': currency.value.upper(),
            'description': product.public_title,
            'externalCustomerId': user.pk,
            'handlePayment': False,
            'returnUrl': cls.render_success_redirect_url(order=order)
        }

        response = cls.make_request(
            method='POST',
            url=urljoin(cls.endpoint_url, '/api/v1/merchant/api/transactions'),
            headers={
                'x-api-key': settings.ARK_PAY_API_KEY,
                'signature': cls.generate_signature(payload=payload),
                'Content-Type': 'application/json'
            },
            json=payload,
        )

        order.invoice_id = response['transaction']['id']
        order.payment_url = response['redirectUrl']
        order.expiry_at = timezone.now() + timedelta(hours=3)
        order.extra = json.dumps({
            'fee': response['transaction']['fee'],
            'earning': response['transaction']['earning'],
        })
        order.save()
        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Full creation of an order')

        return order
