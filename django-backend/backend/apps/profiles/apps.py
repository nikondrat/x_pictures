from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save
from django.utils.translation import ugettext_lazy as _

from apps.profiles import signals


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.profiles'
    verbose_name = _('Profiles')

    def ready(self):
        from apps.profiles import models
        post_delete.connect(signals.remove_file_from_s3, sender=models.Profile)
        post_save.connect(signals.deactivate_subscription_after_create_new, sender=models.ProfileSubscription)
        post_delete.connect(signals.deactivate_subscription_after_deleted, sender=models.ProfileSubscription)
