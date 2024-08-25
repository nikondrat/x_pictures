import uuid
from datetime import timedelta
from urllib.parse import urljoin

from django.db import transaction
from django.utils import timezone

from core.users.models import User
from apps.shop.gate import BaseGate, log
from apps.shop.models import Product, GatewayType, Currency, PaymentOrder, PaymentOrderLog

EXTERNAL_STATUSES = {
    'success': PaymentOrder.Status.PAID,
    'cancel': PaymentOrder.Status.CANCEL,
}


class PaymentGate(BaseGate):
    gateway_type = GatewayType.emovegan
    endpoint_url = 'https://3dsgatewayy.com/'
    conversion_callback = False

    @classmethod
    @transaction.atomic()
    def create(cls, user: User, product: Product, currency: Currency, **options) -> PaymentOrder:
        price = product.get_price_by_currency(currency=currency)

        response = cls.make_request(
            method='POST',
            url=urljoin(cls.endpoint_url, '/gateway/payment/create/'),
            headers={
                'Authorization': 'Bearer 5defb89f8d26987e25556410549cc17ac2c7b059e87005132e8dff793239d509',
            },
            data={
                'merchant': f'X-Pictures: {product.public_title}',
                'amount': float(price),
                'currency': currency.value.upper(),
            },
        )

        order = cls.model.objects.create(
            invoice_id=str(uuid.uuid4()),
            payment_url=response['url'],
            user=user,
            gateway_type=cls.gateway_type,
            product=product,
            price=price,
            currency=currency,
            from_shop=options.get('from_shop', False),
            expiry_at=timezone.now() + timedelta(hours=2),
        )

        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Create order')

        return order
