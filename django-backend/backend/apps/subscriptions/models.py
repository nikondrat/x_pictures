from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string


class Subscription(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    uniq_name = models.CharField(_('Unique name'), max_length=255, unique=True)
    price_usd = models.DecimalField(_('Price USD'), max_digits=255, decimal_places=2, default=0.0)

    service_path = models.CharField(_('Service path'), max_length=255)

    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self):
        return f'{self.title}'

    @property
    def service(self):
        return import_string(self.service_path)


class UserSubscription(models.Model):
    user_id = models.CharField(_('User id'), max_length=10)
    subscription = models.ForeignKey(Subscription, verbose_name=_('Subscription'), related_name='subscriptions',
                                     on_delete=models.CASCADE)
    start_period = models.DateTimeField(_('Start period'), default=timezone.now)
    end_period = models.DateTimeField(_('End period'))
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('User subscription')
        verbose_name_plural = _('User subscriptions')

    @property
    def user(self):
        from core.users.models import User
        return User.objects.filter(pk=self.user_id).first()

    def save(self, *args, **kwargs):
        if self.subscription.id != 1:
            from apps.accounts.models import GenerationJob
            GenerationJob.objects.filter(user_id=self.user_id, has_blur=True).update(
                has_blur=False,
            )
        super().save(*args, **kwargs)

    @property
    def service(self):
        return self.subscription.service

    @property
    def is_expired(self):
        return self.end_period <= timezone.now()
