from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from django.conf import settings
from django.utils import timezone

from apps.profiles.models import ProfileType, Profile, ProfileSubscription
from apps.profiles.factories import ProfileFactory, ProfileSubscriptionFactory
from apps.shop.factories import PaymentOrderFactory
from apps.shop.models import PaymentOrder, Product, GatewayType


@pytest.mark.django_db
def test_close_timeout_payments_task(send_celery_task):
    PaymentOrder.objects.all().delete()
    assert PaymentOrder.objects.count() == 0

    product = Product.objects.get(pk=3)

    with freeze_time(datetime(2023, 12, 1)):
        expiry_at = timezone.now() + timedelta(hours=3)
        order1 = PaymentOrderFactory(product=product, gateway_type=GatewayType.ivendpay,
                                     status=PaymentOrder.Status.CREATED, expiry_at=expiry_at)
        order2 = PaymentOrderFactory(product=product, gateway_type=GatewayType.paypal,
                                     status=PaymentOrder.Status.CREATED, expiry_at=expiry_at)
        order3 = PaymentOrderFactory(product=product, gateway_type=GatewayType.payadmit,
                                     status=PaymentOrder.Status.CREATED, expiry_at=expiry_at)

    order4 = PaymentOrderFactory(product=product, gateway_type=GatewayType.payadmit,
                                 status=PaymentOrder.Status.CREATED, expiry_at=timezone.now() + timedelta(hours=3))

    assert order1.is_expired and order1.status == PaymentOrder.Status.CREATED
    assert order2.is_expired and order2.status == PaymentOrder.Status.CREATED
    assert order3.is_expired and order3.status == PaymentOrder.Status.CREATED
    assert not order4.is_expired and order4.status == PaymentOrder.Status.CREATED

    assert PaymentOrder.objects.filter(status=PaymentOrder.Status.CREATED).count() == 4

    send_celery_task('shop:close-timeout-payments:task')

    assert PaymentOrder.objects.get(pk=order1.pk).status == PaymentOrder.Status.CANCEL
    assert PaymentOrder.objects.get(pk=order2.pk).status == PaymentOrder.Status.CANCEL
    assert PaymentOrder.objects.get(pk=order3.pk).status == PaymentOrder.Status.CANCEL
    assert PaymentOrder.objects.get(pk=order4.pk).status == PaymentOrder.Status.CREATED

    assert PaymentOrder.objects.filter(status=PaymentOrder.Status.CREATED).count() == 1


@pytest.mark.django_db
def test_admin_notify_after_paid_task(send_celery_task, mocker):
    product = Product.objects.get(pk=3)
    order = PaymentOrderFactory(product=product, gateway_type=GatewayType.payadmit,
                                status=PaymentOrder.Status.PAID)

    def mock_send_task(name: str, kwargs):
        assert name == 'telegram:send-text-message:task'
        assert kwargs['telegram_token'] == settings.TELEGRAM_BOTS['payment-notify']['api_key']
        assert kwargs['chat_ids'] == settings.TELEGRAM_BOTS['payment-notify']['admin_chat_ids']

    mocker.patch(
        'apps.shop.tasks.current_app.send_task',
        new=mock_send_task
    )

    send_celery_task('apps.shop.tasks.admin_notify_after_paid_task', kwargs={'order_id': order.id})


@pytest.mark.django_db
@pytest.mark.parametrize('gateway_type', [
    GatewayType.paypal,
    GatewayType.patreon,
    GatewayType.payadmit,
    GatewayType.ivendpay,
])
def test_check_active_subscriptions_task_one_pay_gateway(gateway_type, send_celery_task):
    subscription = Product.objects.get(id=4)

    profile1 = ProfileFactory()
    profile1_subscription = ProfileSubscriptionFactory(
        profile=profile1,
        subscription=subscription,
        end_period=timezone.now() - timedelta(days=15)
    )
    assert profile1.type == ProfileType.premium

    PaymentOrderFactory(
        product=subscription,
        status=PaymentOrder.Status.PAID,
        gateway_type=gateway_type,
        user_id=profile1_subscription.profile_id
    )

    send_celery_task('check-active-subscriptions-task',
                     kwargs={'profile_subscription_id': profile1_subscription.pk})

    assert Profile.objects.get(pk=profile1.pk).type == ProfileType.basic
    assert not ProfileSubscription.objects.get(pk=profile1_subscription.pk).is_active

    assert not ProfileSubscription.objects.filter(
        profile=profile1,
        is_active=True,
    ).exists()


@pytest.mark.django_db
@pytest.mark.parametrize('subscription_status, after_profile_type, has_active_subscription', [
    (True, ProfileType.premium, True),
    (False, ProfileType.basic, False),
])
@pytest.mark.parametrize('gateway_type', [
    GatewayType.paypal_subscription,
    # GatewayType.stripe,
])
def test_check_active_subscriptions_task_subscription_gateway(subscription_status, after_profile_type,
                                                              has_active_subscription, gateway_type,
                                                              send_celery_task, mocker):
    subscription = Product.objects.get(id=4)

    profile1 = ProfileFactory()
    profile1_subscription = ProfileSubscriptionFactory(
        profile=profile1,
        subscription=subscription,
        end_period=timezone.now() - timedelta(days=15)
    )
    assert profile1.type == ProfileType.premium

    order: PaymentOrder = PaymentOrderFactory(
        product=subscription,
        status=PaymentOrder.Status.PAID,
        sub_id='fake_sub_id',
        gateway_type=gateway_type,
        user_id=profile1_subscription.profile_id
    )

    if gateway_type == GatewayType.stripe:
        mocker.patch(
            'apps.shop.gate.stripe.PaymentGate.check_subscription_status',
            return_value=subscription_status,
        )
    elif gateway_type == GatewayType.paypal_subscription:
        mocker.patch(
            'apps.shop.gate.paypal_subscription.PaymentGate.check_subscription_status',
            return_value=subscription_status,
        )
    else:
        raise AssertionError('Gateway type not found')

    mocker.patch(
        'apps.shop.gate.base._conversion_callback',
        return_value=None,
    )
    mocker.patch(
        'apps.shop.gate.base._after_paid_call_tasks',
        return_value=None,
    )

    send_celery_task('check-active-subscriptions-task',
                     kwargs={'profile_subscription_id': profile1_subscription.pk})

    assert Profile.objects.get(pk=profile1.pk).type == after_profile_type
    assert not ProfileSubscription.objects.get(pk=profile1_subscription.pk).is_active

    if subscription_status:
        assert ProfileSubscription.objects.filter(
            profile=profile1,
            is_active=True,
        ).exists()

        new_order: PaymentOrder = PaymentOrder.objects.exclude(
            pk=order.pk
        ).filter(
            user_id=profile1.pk,
            status=PaymentOrder.Status.PAID,
        ).first()
        assert new_order is not None

        assert new_order.gateway_type == order.gateway_type
        assert new_order.product == order.product
        assert new_order.currency == order.currency
        assert new_order.sub_id == order.sub_id
        assert new_order.invoice_id != order.invoice_id
        assert new_order.payment_url == order.payment_url
        assert new_order.expiry_at == order.expiry_at
        assert new_order.extra == order.extra
