from django.apps import AppConfig
from django.db.models.signals import post_delete
from django.utils.translation import ugettext_lazy as _

from apps.jobs.signals import remove_file_from_s3, job_remove_file_from_s3


class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.jobs'
    verbose_name = _('Jobs')

    def ready(self):
        from apps.jobs import models
        post_delete.connect(remove_file_from_s3, sender=models.Tag)
        post_delete.connect(remove_file_from_s3, sender=models.Category)
        post_delete.connect(remove_file_from_s3, sender=models.Filter)
        post_delete.connect(remove_file_from_s3, sender=models.SDModel)
        post_delete.connect(remove_file_from_s3, sender=models.Action)

        post_delete.connect(job_remove_file_from_s3, sender=models.UndressJob)
        post_delete.connect(job_remove_file_from_s3, sender=models.GenerateJob)
        post_delete.connect(job_remove_file_from_s3, sender=models.VideoJob)
