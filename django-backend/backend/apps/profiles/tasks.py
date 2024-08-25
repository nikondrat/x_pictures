import decimal

from celery import shared_task, current_app

from django.db import transaction
from django.utils import timezone

from core.users.config import DAILY_ACCRUAL_OF_TOKENS
from apps.profiles.models import Profile, ProfileSubscription


@shared_task(name='profile:deactivate-expired-subscriptions:task')
def deactivate_expired_subscriptions_task():
    """Deactivate expired subscriptions"""
    with transaction.atomic():
        for profile_subscription in ProfileSubscription.objects.exclude(
            is_active=False,
        ).filter(
            end_period__lte=timezone.now(),
        ):
            current_app.send_task(
                'check-active-subscriptions-task',
                kwargs={
                    'profile_subscription_id': profile_subscription.pk,
                },
            )


@shared_task(name='profile:distribution-of-free-token:task')
def distribution_of_free_token_task():
    with transaction.atomic():
        Profile.objects.filter(
            owner__is_unique_account=True,
            balance__lt=decimal.Decimal('20'),
        ).update(balance=DAILY_ACCRUAL_OF_TOKENS)
