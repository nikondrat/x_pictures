from __future__ import annotations

import os
import random
import string
import binascii
import datetime
from typing import Optional

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager


def generate_user_id():
    prefix = random.randint(100, 999)
    postfix = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(6))
    return f"{prefix}:{postfix}"


class CustomUserManager(UserManager):
    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user('admin', email, password, **extra_fields)


class User(AbstractUser):
    class AuthProvider(models.TextChoices):
        email = 'email', _('Email')
        google = 'google', _('Google')
        shop = 'shop', _('Shop')

    id = models.CharField(_('ID'), primary_key=True, max_length=10)
    username = models.CharField(_('Username'), max_length=150, default=None, null=True)
    email = models.EmailField(_('Email address'), unique=True)
    email_confirmed = models.BooleanField(_('Email confirmed'), default=False)
    decoded_password = models.CharField(_('Decoded password'), default=None, max_length=128, blank=True, null=True)

    auth_provider = models.CharField(_('Auth provider'), max_length=255, choices=AuthProvider.choices,
                                     default=AuthProvider.email)

    email_before_delete = models.EmailField(_('Email before delete'), default=None, null=True, blank=True)
    deleted_account = models.BooleanField(_('Deleted account'), default=False)

    is_unique_account = models.BooleanField('Unique account', default=True)
    ip_address = models.CharField(_('IP address'), max_length=255, null=True, blank=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def is_verified(self) -> bool:
        return self.email_confirmed

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def has_patreon_account(self) -> bool:
        return hasattr(self, 'patreon')

    @property
    def click_id(self) -> Optional[str]:
        if hasattr(self, 'alanbase'):
            return self.alanbase.click_id


class EmailMessage(models.Model):
    class MessageType(models.IntegerChoices):
        verification = 1, _('Verification')         # Email Confirmation
        password_reset = 2, _('Password reset')

    class Status(models.IntegerChoices):
        CREATE = 0, _('Create')
        SENT = 1, _('Sent')
        SUCCESS = 2, _('Success')
        ERROR = -1, _('Error')
        CANCEL = -2, _('Cancel')

    key = models.CharField(_('Secret key'), max_length=50, unique=True, primary_key=True)
    user_id = models.CharField(_('User ID'), max_length=10, default=None, blank=True, null=True)
    email = models.EmailField(_('Email'), default=None, blank=True, null=True)
    type = models.IntegerField(_('Message type'), choices=MessageType.choices, default=MessageType.verification)
    status = models.IntegerField(_('Status'), choices=Status.choices, default=Status.CREATE)
    created = models.DateTimeField(_('Created'), auto_now=True)

    class Meta:
        verbose_name = _('Email message')
        verbose_name_plural = _('Email messages')

    def __str__(self):
        return f'Email: {self.user_id} : {self.get_type_display()}'

    @classmethod
    def generate_secret_key(cls) -> str:
        return binascii.hexlify(os.urandom(20)).decode()

    @property
    def is_confirmed(self) -> bool:
        return self.status in (self.Status.SUCCESS, self.Status.CANCEL, self.Status.ERROR)

    @property
    def template(self) -> str:
        match self.type:
            case self.MessageType.verification:
                template_name = 'verification'
            case self.MessageType.password_reset:
                template_name = 'password_reset'
            case _:
                raise ValueError('Template not found!')

        return f'emails/{template_name}.html'

    @property
    def subject(self) -> str:
        match self.type:
            case self.MessageType.verification:
                return 'Verification'
            case self.MessageType.password_reset:
                return 'Reset password'
            case _:
                raise ValueError('Subject not found!')

    @property
    def from_email(self) -> str:
        match self.type:
            case self.MessageType.verification:
                return settings.EMAIL_HOST_USER
            case self.MessageType.password_reset:
                return settings.EMAIL_HOST_USER
            case _:
                raise ValueError('From email not found!')

    @property
    def to_email(self) -> str:
        return self.email

    @property
    def user(self):
        return User.objects.get(pk=self.user_id)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode()
        super().save(*args, **kwargs)


class Token(models.Model):
    key = models.CharField(_('Token'), max_length=50, primary_key=True)
    user_id = models.CharField(_('User ID'), max_length=10)
    created = models.DateTimeField(_('Created'), auto_now=True)

    lifetime = datetime.timedelta(hours=24*30)

    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')

    @classmethod
    def expired_qs(cls):
        return cls.objects.filter(created__lt=timezone.now() - cls.lifetime)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return f'Token: {self.user_id}'

    @property
    def user(self) -> User:
        from core.users.utils import get_user_by_id
        return get_user_by_id(user_id=self.user_id)

    @property
    def expires(self) -> datetime:
        return self.created + self.lifetime

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expires

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = self.generate_key()
        super().save(*args, **kwargs)


class AlanBase(models.Model):
    user = models.OneToOneField(User, verbose_name=_('User'), on_delete=models.CASCADE,
                                related_name='alanbase')
    click_id = models.CharField(_('Clik id'), max_length=255, default=None, null=True, blank=True)

    sub_id5 = models.CharField(_('Sub id #5'), max_length=255, default=None, null=True, blank=True)

    class Meta:
        verbose_name = _('Alan Base')
        verbose_name_plural = _('Alan Base')
