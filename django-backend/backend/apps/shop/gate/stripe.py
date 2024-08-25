import json
from datetime import datetime
from urllib.parse import urljoin

import jwt
import stripe

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.request import Request

from core.common.utils import get_logger
from core.users.models import User
from apps.profiles.models import Profile
from apps.shop.gate.base import BaseGate, log
from apps.shop.models import Product, ProductType, Price, Currency
from apps.shop.models import GatewayType, PaymentOrder, PaymentOrderLog, StripeCustomer

logger = get_logger('gate:stripe')


def encode_checkout_token(pk: str, status: int) -> str:
    return jwt.encode(
        payload={
            'pk': str(pk),
            'status': status,
        },
        key=settings.STRIPE_API_KEY,
        algorithm='HS256',
    )


def decode_checkout_token(checkout_token: str) -> dict:
    try:
        return jwt.decode(
            jwt=checkout_token,
            key=settings.STRIPE_API_KEY,
            algorithms=['HS256'],
        )
    except Exception:
        raise exceptions.ValidationError({
            'checkout_token': _('Invalid token!')
        })


class PaymentGate(BaseGate):
    gateway_type = GatewayType.stripe

    if hasattr(settings, 'NGROK_DOMAIN'):
        domain = settings.NGROK_DOMAIN
    else:
        domain = settings.SHOP_DOMAIN

    @classmethod
    def get_event(cls, request: Request):
        try:
            return stripe.Webhook.construct_event(
                api_key=settings.STRIPE_API_KEY,
                payload=request.data,
                sig_header=request.META.get('HTTP_STRIPE_SIGNATURE'),
                secret=settings.STRIPE_WEBHOOK_KEY,
            )
        except ValueError:
            raise exceptions.ValidationError({
                'signature': _('Invalid signature'),
            })
        except stripe.error.SignatureVerificationError:
            raise exceptions.ValidationError({
                'signature': _('Invalid signature'),
            })

    @classmethod
    def get_or_create_customer(cls, user: User) -> tuple[StripeCustomer, bool]:
        is_created = False
        customer = StripeCustomer.objects.filter(owner=user).first()
        if not customer:
            raw_customer = stripe.Customer.create(
                api_key=settings.STRIPE_API_KEY,
                email=user.email,
            )
            is_created = True
            customer = StripeCustomer.objects.create(id=raw_customer.id, owner=user)
        return (customer, is_created)

    @classmethod
    def get_prices(cls, product: Product, currency: Currency):
        obj = Price.objects.get(product=product, currency=currency)
        return obj.price, obj.stripe_price_id

    @classmethod
    @transaction.atomic()
    def create(cls, user: User, product: Product, currency: Currency, **options) -> PaymentOrder:
        price, stripe_price_id = cls.get_prices(product=product, currency=currency)

        mode = 'subscription' if product.type == ProductType.subscription else 'payment'
        customer, is_created = cls.get_or_create_customer(user=user)

        order = cls.model.objects.create(
            user=user,
            gateway_type=cls.gateway_type,
            product=product,
            price=price,
            currency=currency,
            from_shop=options.get('from_shop', False),
        )

        if is_created:
            log(order=order,
                action=PaymentOrderLog.Action.INFO,
                text=f'Create customer: {customer.id}')

        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Creating an order object')

        callback_url = urljoin(cls.domain, reverse('stripe_callback'))
        success_checkout_token = encode_checkout_token(pk=order.pk, status=cls.model.Status.PAID)
        cancel_checkout_token = encode_checkout_token(pk=order.pk, status=cls.model.Status.CANCEL)

        response = stripe.checkout.Session.create(
            api_key=settings.STRIPE_API_KEY,
            line_items=[{
                'price': stripe_price_id,
                'quantity': 1,
            }],
            mode=mode,
            success_url=urljoin(callback_url, f'?checkout_token={success_checkout_token}'),
            cancel_url=urljoin(callback_url, f'?checkout_token={cancel_checkout_token}'),
            customer=customer.id,
        )

        order.invoice_id = response.id
        order.payment_url = response.url
        order.expiry_at = timezone.make_aware(datetime.fromtimestamp(response.expires_at))
        order.extra = json.dumps({
            'mode': mode,
            'customer_id': customer.id,
            'stripe_price_id': stripe_price_id,
        })
        order.save()
        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Full creation of an order')

        return order

    @classmethod
    def after_paid(cls, profile: Profile, order: PaymentOrder):
        if (
                order.product.type == ProductType.subscription and
                order.sub_id is None
        ):
            response = stripe.checkout.Session.retrieve(
                api_key=settings.STRIPE_API_KEY,
                id=order.invoice_id
            )
            order.sub_id = response.subscription
            order.save()
            log(order=order,
                action=PaymentOrderLog.Action.INFO,
                text='Capture checkout payment after subscribing')

        super().after_paid(profile=profile, order=order)

    @classmethod
    @transaction.atomic()
    def cancel_subscription(cls, order: PaymentOrder):
        super().cancel_subscription(order=order)

        try:
            stripe.Subscription.cancel(
                order.sub_id,
                api_key=settings.STRIPE_API_KEY,
            )
            log(order=order,
                action=PaymentOrderLog.Action.INFO,
                text='Disable subscription')
        except Exception as err:
            logger.error(f'Stripe :: Cancel subscription :: Error: {err}')
            raise exceptions.APIException({
                'detail': _('Error on Stripe')
            })

    @classmethod
    @transaction.atomic()
    def check_subscription_status(cls, order: PaymentOrder):
        super().check_subscription_status(order=order)
        subscription = stripe.Subscription.retrieve(
            id=order.sub_id,
            api_key=settings.STRIPE_API_KEY,
        )
        status = subscription.status == 'active'
        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text=f'Checking subscription: {status}')
        return status
