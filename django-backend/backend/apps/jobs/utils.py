from celery import current_app
from django.conf import settings

from apps.jobs.models import GenerateJob, ImageGallery
from apps.jobs.models import VideoJob, VideoGallery


def save_to_image_gallery(job: GenerateJob) -> ImageGallery:
    if settings.ADD_IMAGE_TO_GALLERY:
        return current_app.send_task(
            'jobs:add-to-gallery:task',
            kwargs=dict(
                gallery_type='image',
                job_pk=str(job.pk)
            ),
        )


def save_to_video_gallery(job: VideoJob) -> VideoGallery:
    if settings.ADD_VIDEO_TO_GALLERY:
        return current_app.send_task(
            'jobs:add-to-gallery:task',
            kwargs=dict(
                gallery_type='video',
                job_pk=str(job.pk)
            ),
        )
