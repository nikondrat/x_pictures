from urllib.parse import urljoin
from datetime import datetime

from celery import shared_task, current_app
# from django.core import mail
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

# from django.utils.html import strip_tags
# from django.utils.translation import gettext as _
# from django.template.loader import render_to_string

from core.common.utils import get_logger
from apps.profiles.models import ProfileSubscription, Patreon
from apps.shop.models import PaymentOrder, Product, PaymentOrderLog, GatewayType, Currency
from apps.shop.gate import get_payment_gateway, log

logger = get_logger('shop:tasks')


@shared_task(name='shop:close-timeout-payments:task')
def close_timeout_payments_task():
    for order in PaymentOrder.objects.filter(status=PaymentOrder.Status.CREATED):
        if order.is_expired:
            gate = get_payment_gateway(gateway_type=order.gateway_type)
            gate.update(
                order=order,
                status=PaymentOrder.Status.CANCEL,
                external_status='TIMEOUT',
            )


@shared_task(name='shop:unsent-payment-messages:task')
def unsent_payment_messages_task():
    for order in PaymentOrder.objects.filter(status=PaymentOrder.Status.PAID,
                                             is_sent_email=False):
        current_app.send_task(
            'apps.shop.tasks.user_notify_after_paid_task',
            kwargs={'order_id': str(order.id)}
        )


@shared_task(name='shop:admin-notify-after-paid:task')
def admin_notify_after_paid_task(order_id: str):
    order = PaymentOrder.objects.get(pk=order_id)

    order_admin_url = reverse(f'admin:{order._meta.app_label}_{order._meta.model_name}_change',
                              args=[order.pk])
    user_admin_url = reverse(f'admin:{order.user._meta.app_label}_{order.user._meta.model_name}_change',
                             args=[order.user_id])

    # Telegram notify
    current_app.send_task(
        'telegram:send-text-message:task',
        kwargs={
            'telegram_token': settings.TELEGRAM_BOTS['payment-notify']['api_key'],
            'chat_ids': settings.TELEGRAM_BOTS['payment-notify']['admin_chat_ids'],
            'text': (
                f'🟢 Произошла покупка: <b>{order.product.title}</b>\n'
                f'Пользователь: <a href="{urljoin(settings.DOMAIN, user_admin_url)}">{order.user.email}</a>\n'
                f'Платежный шлюз: <b>{order.get_gateway_type_display()}</b>\n'
                f'Сумма: <b>{order.price} {order.get_currency_display()}</b>\n'
                f'Дата и время: <b>{order.updated.strftime("%d.%m.%Y, %H:%M:%S")}</b>'
            ),
            'keyboard': {
                'inline_keyboard': [[
                    {'text': '📑 Ордер', 'url': urljoin(settings.DOMAIN, order_admin_url)},
                ]]
            }
        }
    )
    log(order=order,
        action=PaymentOrderLog.Action.INFO,
        text='Admin Notification after paid')

    return True


@shared_task
def user_notify_after_paid_task(order_id: str):
    # order = PaymentOrder.objects.get(pk=order_id)
    #
    # html_message = render_to_string('emails/successful_payment.html', {
    #     'order': order,
    # })
    # plain_message = strip_tags(html_message)
    #
    # email = mail.EmailMultiAlternatives(
    #     subject=_('Successful payment'),
    #     body=plain_message,
    #     from_email=settings.EMAIL_HOST_USER,
    #     to=[order.user.email],
    #     connection=mail.get_connection(),
    # )
    # email.attach_alternative(html_message, 'text/html')
    #
    # try:
    #     book_path = order.book_pdf
    #     if book_path:
    #         email.attach_file(book_path)
    # except Exception as err:
    #     log(order=order,
    #         action=PaymentOrderLog.Action.ERROR,
    #         text=f'Not found book: {err}')
    #
    # try:
    #     status = email.send()
    #     order.is_sent_email = True
    #     order.save()
    #     log(order=order,
    #         action=PaymentOrderLog.Action.INFO,
    #         text=(
    #             f'The book has been successfully sent to: {order.user.email}\n'
    #             f'Book name: {order.book_name}'
    #         ))
    # except Exception as err:
    #     status = False
    #     log(order=order,
    #         action=PaymentOrderLog.Action.ERROR,
    #         text=f'The email could not be sent: {err}')
    #
    # return status
    return True


@shared_task(name='check-active-subscriptions-task')
def check_active_subscriptions_task(profile_subscription_id: int):
    from apps.profiles.utils import has_active_subscription

    profile_subscription = ProfileSubscription.objects.get(pk=profile_subscription_id)

    if has_active_subscription(profile=profile_subscription.profile):
        return True

    order: PaymentOrder = PaymentOrder.objects.filter(product=profile_subscription.subscription,
                                                      status=PaymentOrder.Status.PAID,
                                                      user_id=profile_subscription.profile_id).last()

    if not order or order.gateway_type in [GatewayType.paypal,
                                           GatewayType.payadmit,
                                           GatewayType.patreon,
                                           GatewayType.ivendpay,
                                           GatewayType.stripe]:
        logger.info(f'Deactivate subscription :: User ID: {profile_subscription.profile}\n'
                    f'Reason: The payment system does not support subscriptions')
        profile_subscription.is_active = False
        profile_subscription.save()
        return True
    else:
        gate = order.gateway
        if not gate.check_subscription_status(order=order):
            logger.info(f'Deactivate subscription :: User ID: {profile_subscription.profile}\n'
                        f'Reason: Subscription has expired and has not been paid')
            profile_subscription.is_active = False
            profile_subscription.save()
            return True

        gate.refresh_subscription(order=order)
        logger.info(f'Refresh subscription :: User ID: {profile_subscription.profile}')
        return True


@shared_task(name='shop:include_patreon:task')
def include_patreon_task(patreon_id: str):
    from apps.shop.gate import PatreonPaymentGate

    patreon = Patreon.objects.select_related(
        'profile', 'profile__owner'
    ).get(pk=patreon_id)

    logger.info(f'Include patreon: {patreon.profile_id}')

    gate: PatreonPaymentGate = get_payment_gateway(gateway_type=GatewayType.patreon)

    patreon, is_member = gate.activate_patreon(patreon=patreon)

    return is_member


@shared_task(name='shop:check_patreon_subscription:task')
def check_patreon_subscription_task():
    from apps.shop.gate import PatreonPaymentGate

    members = Patreon.objects.select_related('profile').exclude(
        profile__owner_id='000:000000',
    ).all()

    logger.info(f'Members count: {len(members)}')

    gate: PatreonPaymentGate = get_payment_gateway(gateway_type=GatewayType.patreon)

    data = gate.get_patreon_campaign_info()

    total_members = []
    for member in members:
        logger.info(f'Patreon: {member.profile_id} :: Member: {member.member_id} :: Patreon ID: {member.patreon_id}')
        is_member = member.patreon_id and member.member_id
        if not is_member:
            member, is_member = gate.activate_patreon(patreon=member)

        if is_member:
            total_members.append(member)

    gate.search_v2(members=total_members, data=data)

    return True
