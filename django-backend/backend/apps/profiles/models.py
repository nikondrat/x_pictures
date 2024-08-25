from datetime import timedelta

from django.db import models, transaction
from django.core.validators import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.users.models import User
from core.common.mixins import ImageMixin
from core.common.utils import PathAndRename
from apps.shop.models import Product


class ProfileType(models.TextChoices):
    basic = 'basic', _('Basic')
    advance = 'advance', _('Advance')
    premium = 'premium', _('Premium')
    super_premium = 'super_premium', _('Super Premium')


class ProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            deleted__isnull=True,
        )


class Profile(ImageMixin, models.Model):
    owner = models.OneToOneField(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='profile',
                                 primary_key=True)

    image = models.ImageField(_('Image'), upload_to=PathAndRename('profiles/'), default=None, blank=True, null=True)
    balance = models.DecimalField(_('Balance'), decimal_places=2, max_digits=25, default=2.5)
    type = models.CharField(_('Type'), max_length=255, choices=ProfileType.choices, default=ProfileType.basic)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)
    deleted = models.DateTimeField(_('Deleted'), default=None, null=True, blank=True)

    objects = ProfileManager()
    objects_with_deleted = models.Manager()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return self.owner.id

    def delete(self, using=None, keep_parents=False):
        self.deleted = timezone.now()
        self.save()

    @property
    def is_premium(self) -> bool:
        return self.type in (ProfileType.premium, ProfileType.super_premium)

    @property
    def is_free(self) -> bool:
        return self.type == ProfileType.basic

    @property
    def allowed_images_in_storage(self) -> int:
        return {
            ProfileType.basic: 5,
            ProfileType.advance: 10,
            ProfileType.premium: 100,
            ProfileType.super_premium: 300,
        }[self.type]

    @property
    def has_patreon(self) -> bool:
        return Patreon.objects.filter(profile_id=self.pk).exists()


def profile_subscription_validator(product_id: int):
    if product_id not in (1, 2, 3, 4, 5, 6, 12):
        raise ValidationError(_('The product must be a subscription'))


class ProfileSubscription(models.Model):
    profile = models.ForeignKey(Profile, verbose_name=_('Profile'), on_delete=models.CASCADE,
                                related_name='subscriptions')
    subscription = models.ForeignKey(Product, verbose_name=_('Subscription product'), on_delete=models.DO_NOTHING,
                                     related_name='profiles', validators=[profile_subscription_validator])
    is_active = models.BooleanField(_('Active'), default=True)
    start_period = models.DateTimeField(_('Start period'), auto_now_add=True)
    end_period = models.DateTimeField(_('End period'), null=True, blank=True)

    class Meta:
        verbose_name = _('Profile subscription')
        verbose_name_plural = _('Profiles subscription')

    @property
    def is_expired(self) -> bool:
        return self.end_period <= timezone.now()

    @transaction.atomic()
    def save(self, *args, **kwargs):
        if not self.end_period:
            self.end_period = timezone.now() + timedelta(seconds=self.subscription.lifetime)
        if not self.is_active:
            self.profile.type = ProfileType.basic
            self.profile.save()
        super().save(*args, **kwargs)


class Patreon(models.Model):
    profile = models.OneToOneField(Profile, verbose_name=_('Profile'), on_delete=models.CASCADE,
                                   related_name='patreon')

    access_token = models.CharField(_('Access token'), max_length=255)
    refresh_token = models.CharField(_('Refresh token'), max_length=255)

    expires_in = models.DateTimeField(_('Expires in'))
    scope = models.CharField(_('scope'), max_length=255)
    token_type = models.CharField(_('Token type'), default='Bearer', max_length=255)

    patreon_id = models.IntegerField(_('Patreon ID'), default=None, blank=True, null=True)
    member_id = models.UUIDField(_('Member ID'), default=None, blank=True, null=True)

    class Meta:
        verbose_name = _('Patreon')
        verbose_name_plural = _('Patreon')

    def __str__(self):
        return f'Patreon: {self.profile.pk}'

    @property
    def is_admin(self) -> bool:
        return self.profile.pk == '000:000000'

    @property
    def is_expired(self) -> bool:
        return self.expires_in <= timezone.now()

    @property
    def auth_token(self) -> str:
        return f'{self.token_type} {self.access_token}'
