from typing import Type

from apps.shop.models import GatewayType

from .base import BaseGate, log
from .ivendpay import PaymentGate as IvendPayPaymentGate
from .paypal import PaymentGate as PaypalPaymentGate
from .paypal_subscription import PaymentGate as PaypalSubscriptionPaymentGate
from .payadmit import PaymentGate as PayAdmitPaymentGate
from .stripe import PaymentGate as StripePaymentGate
from .emovegan import PaymentGate as EmoveganPaymentGate
from .ark_pay import PaymentGate as ArkPayPaymentGate
from .patreon import PaymentGate as PatreonPaymentGate

order_log = log     # alias

gateway_classes = {
    GatewayType.ivendpay: IvendPayPaymentGate,
    GatewayType.paypal: PaypalPaymentGate,
    GatewayType.paypal_subscription: PaypalSubscriptionPaymentGate,
    GatewayType.payadmit: PayAdmitPaymentGate,
    GatewayType.stripe: StripePaymentGate,
    GatewayType.emovegan: EmoveganPaymentGate,
    GatewayType.ark_pay: ArkPayPaymentGate,
    GatewayType.patreon: PatreonPaymentGate,
}


def get_payment_gateway(gateway_type: GatewayType) -> Type[BaseGate]:
    return gateway_classes[gateway_type]
