from django.db import transaction

from core.common.cached.ram import Cached
from core.users.models import User
from apps.shop.gate import get_payment_gateway
from apps.shop.models import Currency, GatewayType, PaymentOrder


@Cached(timeout=60 * 60)
def get_gateway_types_by_currency(currency: Currency) -> list[Currency]:
    gates = {
        Currency.USD: [GatewayType.ivendpay,
                       # GatewayType.paypal,
                       # GatewayType.payadmit,
                       # GatewayType.stripe
                       # GatewayType.emovegan,
                       # GatewayType.ark_pay
                       ],
        Currency.RUB: [GatewayType.ivendpay]
    }

    return gates[currency]


@transaction.atomic()
def cancel_subscription(user: User):
    profile_subscription = user.profile.subscriptions.filter(
        is_active=True,
    ).first()
    profile_subscription.is_active = False

    order: PaymentOrder = PaymentOrder.objects.select_related(
        'user', 'product',
    ).filter(
        user=user,
        product=profile_subscription.subscription,
        status=PaymentOrder.Status.PAID,
    ).last()

    if order and order.gateway_type in [GatewayType.paypal_subscription, GatewayType.stripe]:
        gate = get_payment_gateway(gateway_type=order.gateway_type)
        gate.cancel_subscription(order=order)

    profile_subscription.save()
