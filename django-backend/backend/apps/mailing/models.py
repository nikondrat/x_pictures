import os
import binascii

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from core.users.models import User


class Event(models.TextChoices):
    first_event_2024 = 'first_event_2024', _('First Event (Free tokens)')


class Message(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, _('Created')
        SENT = 1, _('Sent')
        SUCCESS = 2, _('Success')
        EXPIRED = 3, _('Expired')
        ERROR = -1, _('Error')

    event = models.CharField(_('Event'), choices=Event.choices, max_length=255)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    status = models.IntegerField(_('Status'), choices=Status.choices, default=Status.CREATED)

    secret_code = models.CharField(_('Secret code'), max_length=255, unique=True)

    expiry_at = models.DateTimeField(_('Expiry at'), null=True, blank=True, default=None)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)

    class Meta:
        verbose_name = _('Event message')
        verbose_name_plural = _('Event messages')

    @classmethod
    def generate_secret_code(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):
        if not self.secret_code:
            self.secret_code = self.generate_secret_code()
        super().save(*args, **kwargs)

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expiry_at
