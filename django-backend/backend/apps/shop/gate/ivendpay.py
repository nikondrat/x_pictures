import json
from typing import Optional
from datetime import datetime
from urllib.parse import urljoin

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions

from core.users.models import User
from apps.shop.gate.base import BaseGate, log
from apps.shop.models import Product, Currency, GatewayType, PaymentOrder, PaymentOrderLog


EXTERNAL_STATUSES = {
    'CANCELED': PaymentOrder.Status.CANCEL,
    'TIMEOUT': PaymentOrder.Status.CANCEL,
    'PAID': PaymentOrder.Status.PAID,
}


class PaymentGate(BaseGate):
    endpoint_url = 'https://gate.ivendpay.com/'
    gateway_type = GatewayType.ivendpay

    @classmethod
    def make_request(cls, method: str, url: str, headers: Optional[dict] = None, **kwargs):
        response = super(PaymentGate, cls).make_request(
            method=method, url=url, headers={
                'X-API-KEY': settings.IVENDPAY_API_KEY,
            },
            **kwargs,
        )
        return response['data'][0]

    @classmethod
    def validate_options(cls, options: dict):
        if not options.get('crypto_currency'):
            raise exceptions.ValidationError({
                'extra_data': {
                    'crypto_currency': _('No cryptocurrency is specified')
                }
            })

    @classmethod
    @transaction.atomic()
    def create(cls, user: User, product: Product, currency: Currency, **options) -> PaymentOrder:
        cls.validate_options(options=options)
        price = product.get_price_by_currency(currency=currency)

        response = cls.make_request(
            method='POST',
            url=urljoin(cls.endpoint_url, '/api/v3/create'),
            json={
                'currency': options['crypto_currency'],
                'amount_fiat': '%.2f' % price,
                'currency_fiat': currency.value.upper(),
            },
        )

        order = cls.model.objects.create(
            invoice_id=response['invoice'],
            payment_url=response['payment_url'],
            user=user,
            gateway_type=cls.gateway_type,
            product=product,
            price=price,
            currency=currency,
            from_shop=options.get('from_shop', False),
            extra=json.dumps({
                'crypto_currency': response['currency'],
                'crypto_amount': response['amount'],
            }, default=str),
            expiry_at=timezone.make_aware(datetime.fromtimestamp(response['expiry_at'])),
        )
        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Create order')

        return order
