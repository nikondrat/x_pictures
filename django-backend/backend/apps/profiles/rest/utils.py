import io
import uuid
from datetime import timedelta

import faker
from mimetypes import guess_type
from celery import current_app

from django.db import transaction
from django.utils import timezone
from django.core.files.base import ContentFile
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from rest_framework import exceptions

from core.common.cached.ram import Cached
from core.users.models import User, Token
from apps.profiles.models import Profile, Patreon
from apps.jobs.models import GenerateJob, VideoJob
from apps.jobs.models import ImageGallery, VideoGallery, Like


@transaction.atomic()
def delete_account(user: User):
    Token.objects.filter(user_id=user.pk).delete()

    user.email_before_delete = user.email
    user.email = faker.Faker().unique.email()
    user.deleted_account = True

    profile = user.profile

    profile.delete()
    user.save()


@transaction.atomic()
def change_password(user: User, new_password: str) -> User:
    user.decoded_password = new_password
    user.password = make_password(new_password)
    user.save()
    return user


@Cached(timeout=60*2)
def get_image_storage_qs(profile: Profile) -> list[GenerateJob]:
    return GenerateJob.objects.filter(
        show_in_profile=True,
        status=GenerateJob.Status.SUCCESS,
        user_id=profile.owner_id,
    ).order_by('-created')[:profile.allowed_images_in_storage]


@Cached(timeout=60*2)
def get_video_storage_qs(profile: Profile) -> list[VideoGallery]:
    return VideoGallery.objects.filter(
        show_in_profile=True,
        status=GenerateJob.Status.SUCCESS,
        user_id=profile.owner_id,
    ).order_by('-created')[:profile.allowed_images_in_storage]


@Cached(timeout=60*2)
def get_liked_images_qs(profile: Profile) -> list[GenerateJob]:
    result = []
    for obj in Like.objects.filter(
            author=profile.owner,
            content_type=ContentType.objects.get_for_model(ImageGallery).id,
            is_active=True
    ):
        result.append(obj.content_object)
    return result


@Cached(timeout=60*2)
def get_liked_video_qs(profile: Profile) -> list[VideoJob]:
    result = []
    for obj in Like.objects.filter(
            author=profile.owner,
            content_type=ContentType.objects.get_for_model(VideoGallery).id,
            is_active=True
    ):
        result.append(obj.content_object)
    return result


@Cached(timeout=15)
def get_generation_count(user: User):
    generates = GenerateJob.objects.filter(status=GenerateJob.Status.SUCCESS, user_id=user.pk).count()
    videos = VideoJob.objects.filter(status=VideoJob.Status.SUCCESS, user_id=user.pk).count()

    return sum([generates, videos])


@transaction.atomic()
def delete_image_from_storage(user: User, pk: uuid.UUID):
    job = GenerateJob.objects.filter(user_id=user.pk, show_in_profile=True).filter(pk=pk).first()
    if not job:
        raise exceptions.ValidationError({
            'pk': _('Job not found')
        })
    job.show_in_profile = False
    job.save()


@transaction.atomic()
def delete_video_from_storage(user: User, pk: uuid.UUID):
    job = VideoJob.objects.filter(user_id=user.pk, show_in_profile=True).filter(pk=pk).first()
    if not job:
        raise exceptions.ValidationError({
            'pk': _('Job not found')
        })
    job.show_in_profile = False
    job.save()


@transaction.atomic()
def delete_image(profile: Profile) -> Profile:
    profile.image.delete()
    return profile


@transaction.atomic()
def upload_image(profile: Profile, image_b64: str) -> Profile:
    from apps.jobs.services import base64_to_image

    image_data = image_b64
    image_format = 'jpeg'
    if len(image_b64.split(',')) > 1:
        _, image_data = image_b64.split(',')
        image_format = guess_type(image_b64)[0].split('/')[1]

    image = base64_to_image(image_b64_data=image_data)
    image = image.resize((480, 480))

    buffer = io.BytesIO()
    image.save(buffer, image_format)
    buffer.seek(0)

    if profile.image:
        delete_image(profile=profile)

    profile.image.save(f'avatar-{profile.pk}.{image_format}',
                       ContentFile(buffer.getvalue()))

    return profile


@transaction.atomic()
def include_patreon(profile: Profile, patreon_info: dict) -> Patreon:
    patreon = Patreon(
        profile=profile,
        access_token=patreon_info['access_token'],
        refresh_token=patreon_info['refresh_token'],
        expires_in=timezone.now() + timedelta(seconds=patreon_info['expires_in']),
        scope=patreon_info['scope'],
        token_type=patreon_info['token_type'],
    )

    transaction.on_commit(
        lambda: current_app.send_task(
            'shop:include_patreon:task',
            kwargs=dict(
                patreon_id=patreon.pk,
            ),
        )
    )

    patreon.save()
    return patreon
