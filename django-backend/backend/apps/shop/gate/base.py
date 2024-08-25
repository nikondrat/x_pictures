import abc
import uuid
import json
import logging
from typing import Optional
from datetime import timedelta
from urllib.parse import urljoin

import requests
from celery import current_app

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.exceptions import NotFound

from core.common.alanbase import client as alanbase_client

from core.users.models import User
from apps.profiles.models import Profile, ProfileSubscription
from apps.shop.models import ProductType, Product, GatewayType, Currency
from apps.shop.models import PaymentOrder, PaymentOrderLog


def log(order: PaymentOrder, action: PaymentOrderLog.Action, text: str, author: Optional[User] = None):
    try:
        order.log.create(action=action,
                         author=author,
                         text=text)
    except Exception as err:
        logging.error(f'Create log: {err}')


def _conversion_callback(order: PaymentOrder):
    if order.gateway_type == GatewayType.paypal_subscription:
        sub_id6 = 'PayPal'
    elif order.gateway_type == GatewayType.patreon:
        sub_id6 = 'Patreon'
    else:
        sub_id6 = order.get_gateway_type_display()

    data = {'sub_id6': sub_id6}
    if hasattr(order.user, 'alanbase') and order.user.alanbase.sub_id5 is not None:
        data.update({
            'sub_id5': order.user.alanbase.sub_id5,
        })

    if order.user.click_id:
        alanbase_client.make_payment(
            click_id=order.user.click_id,
            amount=float(order.price),
            payment_id=str(order.pk),
            **data,
        )
    else:
        alanbase_client.make_payment_without_click_id(
            user_id=order.user_id,
            amount=float(order.price),
            payment_id=str(order.pk),
            **data,
        )

    log(order=order,
        action=PaymentOrderLog.Action.INFO,
        text='Callback in AlanBase')


def _after_paid_call_tasks(order: PaymentOrder):
    try:
        # from apps.shop.tasks import admin_notify_after_paid_task
        # admin_notify_after_paid_task.delay(
        #     order.pk,
        # )
        transaction.on_commit(lambda: current_app.send_task(
            'shop:admin-notify-after-paid:task',
            kwargs=dict(
                order_id=str(order.pk),
            ),
        ))
    except Exception as err:
        log(order=order,
            action=PaymentOrderLog.Action.ERROR,
            text=f'Error sent task admin_notify_after_paid_task: {err}')
    else:
        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text=f'Sent task admin_notify_after_paid_task: SUCCESS')

    # try:
    #     # Send notify to user
    #     from apps.shop.tasks import user_notify_after_paid_task
    #     user_notify_after_paid_task.delay(
    #         order.pk,
    #     )
    # except Exception as err:
    #     log(order=order,
    #         action=PaymentOrderLog.Action.ERROR,
    #         text=f'Error sent task user_notify_after_paid_task: {err}')
    # else:
    #     log(order=order,
    #         action=PaymentOrderLog.Action.INFO,
    #         text=f'Sent task user_notify_after_paid_task: SUCCESS')


class BaseGate(metaclass=abc.ABCMeta):
    model = PaymentOrder
    gateway_type: GatewayType

    endpoint_url: str
    default_headers = {}

    conversion_callback: bool = True

    @classmethod
    def render_success_redirect_url(cls, order: PaymentOrder, *, is_redirect_through_shop: bool = False):
        if order.from_shop:
            return urljoin(settings.FRONT_SHOP_DOMAIN, '/?payment=success')
        elif is_redirect_through_shop:
            url = '/checkout-redirect/?payment=success'
            if order.product.type == ProductType.subscription:
                next_payment = timezone.now() + timedelta(seconds=order.product.lifetime)
                url += '&next_payment={}'.format(next_payment.strftime('%d.%m.%Y'))
            return urljoin(settings.FRONT_SHOP_DOMAIN, url)
        else:
            url = '?payment=success'
            if order.product.type == ProductType.subscription:
                next_payment = timezone.now() + timedelta(seconds=order.product.lifetime)
                url += '&next_payment={}'.format(next_payment.strftime('%d.%m.%Y'))
            return urljoin(settings.FRONT_DOMAIN, url)

    @classmethod
    def render_cancel_redirect_url(cls, order: PaymentOrder, *, is_redirect_through_shop: bool = False):
        if order.from_shop:
            return settings.FRONT_SHOP_DOMAIN
        elif is_redirect_through_shop:
            return urljoin(settings.FRONT_SHOP_DOMAIN, '/checkout-redirect/?payment=cancel')
        else:
            return urljoin(settings.FRONT_DOMAIN, '?payment=cancel')

    @classmethod
    def render_redirect_url(cls, order: PaymentOrder):
        if order.status == PaymentOrder.Status.PAID:
            return cls.render_success_redirect_url(order=order)
        return cls.render_cancel_redirect_url(order=order)

    @classmethod
    def _make_request(cls, method: str, url: str, headers: Optional[dict] = None, *,
                      raise_for_status: bool = True, return_obj: bool = False, **options):
        headers = headers or {}
        headers.update(cls.default_headers)

        response = requests.request(method, url=url, headers=headers, **options)
        print(response)
        if raise_for_status:
            response.raise_for_status()
        if return_obj:
            return response

        return response.json()

    @classmethod
    def make_request(cls, method: str, url: str, headers: Optional[dict] = None, **kwargs) -> dict | requests.Response:
        return cls._make_request(method=method, url=url, headers=headers, **kwargs)

    @classmethod
    @transaction.atomic()
    def after_paid(cls, profile: Profile, order: PaymentOrder, *, is_conversion_callback: bool = True):
        if order.product.type == ProductType.subscription:
            profile_subscription = ProfileSubscription.objects.create(
                profile=profile,
                subscription_id=order.product.id,
                end_period=timezone.now() + timedelta(seconds=order.product.lifetime),
            )
            log(order=order,
                action=PaymentOrderLog.Action.INFO,
                text=f'Creating a subscription for a user: ID: {profile_subscription.pk}')
        else:
            profile.balance += order.product.amount
            profile.save()
            log(order=order,
                action=PaymentOrderLog.Action.INFO,
                text=f'Accrual of tokens to the user`s balance: {order.product.amount}')

        if not settings.DEBUG and cls.conversion_callback and is_conversion_callback:
            _conversion_callback(order=order)

        _after_paid_call_tasks(order=order)

    @classmethod
    def validate_options(cls, options: dict):
        ...

    @classmethod
    @abc.abstractmethod
    def create(cls, user: User, product: Product, currency: Currency, **options) -> PaymentOrder:
        ...

    @classmethod
    @transaction.atomic()
    def update(cls, order: PaymentOrder, status: PaymentOrder.Status, **extra) -> PaymentOrder:
        order.status = status

        for key, value in extra.items():
            if key == 'extra':
                data = json.loads(order.extra)
                data.update(value)
                order.extra = json.dumps(data)
            else:
                setattr(order, key, value)

        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text=f'Update order: Status: {order.get_status_display()} : External status: {order.external_status}')

        if order.is_paid:
            cls.after_paid(order=order,
                           profile=order.user.profile)

        order.save()
        return order

    @classmethod
    def check_subscription_status(cls, order: PaymentOrder) -> bool:
        if not order.product.is_subscription:
            raise NotFound({
                'detail': _('No subscription'),
            })

    @classmethod
    @transaction.atomic()
    def refresh_subscription(cls, order: PaymentOrder) -> PaymentOrder:
        if not order.product.is_subscription:
            raise NotFound({
                'detail': _('No subscription'),
            })

        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text=f'Refresh subscription: {order.sub_id}')

        new_order = cls.model.objects.create(
            user=order.user,
            gateway_type=cls.gateway_type,
            product=order.product,
            price=order.price,
            currency=order.currency,
            sub_id=order.sub_id,
            invoice_id=str(uuid.uuid4()),
            status=PaymentOrder.Status.PAID,
            payment_url=order.payment_url,
            expiry_at=order.expiry_at,
            extra=order.extra,
        )

        cls.after_paid(
            order=new_order,
            profile=new_order.user.profile,
        )
        return new_order

    @classmethod
    def cancel_subscription(cls, order: PaymentOrder):
        if not order.product.is_subscription:
            raise NotFound({
                'detail': _('No subscription'),
            })
