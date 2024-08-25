import json
from urllib.parse import urljoin
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions

from core.users.models import User
from apps.shop.gate.base import BaseGate, log
from apps.shop.models import Product, Currency, GatewayType, PaymentOrder, PaymentOrderLog

EXTERNAL_STATUSES = {
    'CANCELLED': PaymentOrder.Status.CANCEL,
    'DECLINED': PaymentOrder.Status.CANCEL,
    'COMPLETED': PaymentOrder.Status.PAID,
}


class PaymentGate(BaseGate):
    gateway_type = GatewayType.payadmit
    endpoint_url = 'https://app.payadmit.com/'

    if hasattr(settings, 'NGROK_DOMAIN'):
        domain = settings.NGROK_DOMAIN
    else:
        domain = settings.SHOP_DOMAIN

    redirect_url = urljoin(settings.FRONT_DOMAIN, '/profile')

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

        payment_method = options.get('payment_method', 'BASIC_CARD')
        response = cls.make_request(
            method='POST',
            url=urljoin(cls.endpoint_url, '/api/v1/payments'),
            headers={
                'Authorization': f'Bearer {settings.PAYADMIT_SECRET_KEY}',
            },
            json={
                'referenceId': f'order_id={order.pk}',
                'paymentType': 'DEPOSIT',
                'paymentMethod': payment_method,
                'amount': float(price),
                'currency': currency.value.upper(),
                'description': product.public_description,
                'customer': {
                    'referenceId': user.pk,
                    'email': user.email,
                },
                'returnUrl': cls.render_cancel_redirect_url(order=order),
                'successReturnUrl': cls.render_success_redirect_url(order=order),
                'declineReturnUrl': cls.render_cancel_redirect_url(order=order),
                'webhookUrl': urljoin(cls.domain, reverse('payadmit_webhook')),
            },
        )
        if response.get('status') != 200:
            raise exceptions.APIException({
                'detail': _('PayAdmit error')
            })

        result = response['result']

        order.invoice_id = result['id']
        order.payment_url = result['redirectUrl']
        order.expiry_at = timezone.now() + timedelta(hours=3)
        order.extra = json.dumps({
            'payment_method': result['paymentMethod'],
        }, default=str)
        order.save()

        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Full creation of an order')

        return order
