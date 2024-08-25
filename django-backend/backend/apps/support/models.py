from django.db import models
from django.utils.translation import gettext_lazy as _

from core.users.models import User


class SupportMessage(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, _('Created')
        ANSWERED = 1, _('Answered')
        CANCEL = -1, _('Cancel')

    email = models.EmailField(_('Email'))
    name = models.CharField(_('Name'), max_length=255, default=None, blank=True, null=True)
    user_id = models.CharField(_('User ID'), max_length=10)
    message = models.TextField(_('Message'))
    status = models.IntegerField(_('Status'), choices=Status.choices, default=Status.CREATED)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Support message')
        verbose_name_plural = _('Support messages')


class SupportAnswer(models.Model):
    message = models.ForeignKey(SupportMessage, verbose_name=_('Message'), related_name='answers',
                                on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='support_answers', on_delete=models.CASCADE)
    text = models.TextField(_('Message'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Support answer')
        verbose_name_plural = _('Support answers')
