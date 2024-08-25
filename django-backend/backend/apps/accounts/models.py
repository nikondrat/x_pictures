from django.db import models
from django.utils.html import mark_safe
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.users.models import User
from core.users.utils import get_user_by_id


class BaseJOB(models.Model):
    id = models.UUIDField(_('Image id'), primary_key=True)
    user_id = models.CharField(_('User ID'), max_length=10)
    image_url = models.URLField(_('Image url'), default=None, null=True)
    created = models.DateTimeField(_('Created'), default=timezone.now)

    job_type = None

    class Meta:
        abstract = True

    @property
    def user(self) -> User:
        return get_user_by_id(user_id=self.user_id)


class UndressJob(BaseJOB):
    job_type = 'undress'

    class Meta:
        verbose_name = _('Undress job')
        verbose_name_plural = _('Undress jobs')

    @property
    def image(self):
        return mark_safe(f'<img src="https://x-pictures-undress.s3.us-east-2.amazonaws.com/{self.pk}.jpeg" />')


class GenerationJob(BaseJOB):
    prompt = models.CharField(_('Prompt'), max_length=500)
    has_blur = models.BooleanField(_('Has blur'), default=False)
    show_in_profile = models.BooleanField(_('Show in profile'), default=True)

    job_type = 'generate'

    class Meta:
        verbose_name = _('Generation job')
        verbose_name_plural = _('Generation jobs')

    @property
    def image_with_blur_url(self):
        return self.image_url.replace(f'{self.pk}', self.pk.hex)

    @property
    def image(self):
        return mark_safe(f'<img src="{self.image_url}" />')
