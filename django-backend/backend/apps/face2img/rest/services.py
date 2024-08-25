import uuid
from decimal import Decimal
from threading import Thread

from celery import current_app
from rest_framework.exceptions import PermissionDenied
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db import transaction

from apps.face2img import models
from core.users.models import User
from apps.profiles.models import Profile, ProfileType

TRAINING_TIME_SECONDS = 60 * 30
CREATE_FACE2IMG_JOB_ESTIMATED_TIME = 60 * 2

QUEUES = {
    ProfileType.basic: 'vid_basic_queue',
    ProfileType.advance: 'vid_advance_queue',
    ProfileType.premium: 'vid_premium_queue',
    ProfileType.super_premium: 'vid_super_premium_queue',
}


def upload_files_and_start_task(files: list[TemporaryUploadedFile], lora: models.Lora, profile: Profile):
    with transaction.atomic():
        for file in files:
            models.LoraTrainingFace.objects.create(lora=lora, image=file.file)
        lora.status = models.Lora.Status.PROCESS
        lora.save()
        transaction.on_commit(lambda: current_app.send_task(
            'face2img:training-lora:task',
            kwargs=dict(
                pk=str(lora.id),
            ),
            queue=QUEUES[profile.type], # noqa
        ))


def create_lora(user: User, cost: Decimal, files: list[TemporaryUploadedFile]) -> models.Lora:
    profile = user.profile
    if profile.balance < cost:
        raise PermissionDenied("Not enough balance")

    pk = uuid.uuid4()
    user_id = str(user.id)

    postfix_lora_name = f"{user_id}_{str(pk)[:5]}"

    lora_name = f"lora_{postfix_lora_name}"

    with transaction.atomic():
        lora = models.Lora.objects.create(
            id=pk,
            status=models.Lora.Status.CREATED,
            estimated_time=TRAINING_TIME_SECONDS,
            lora_name=lora_name,
            cost=cost,
            user=user,
        )
        profile.balance -= cost
        profile.save()

    Thread(target=upload_files_and_start_task, args=(files, lora)).start()

    return lora


def create_face2img_job(user: User, cost: Decimal, pack: models.Pack, lora: models.Lora) -> models.Face2ImgJob:
    profile = user.profile
    if profile.balance < cost:
        raise PermissionDenied("Not enough balance")

    with transaction.atomic():
        job = models.Face2ImgJob.objects.create(
            user=user,
            lora=lora,
            pack=pack,
            status=models.Face2ImgJob.Status.PROCESS,
            estimated_time=CREATE_FACE2IMG_JOB_ESTIMATED_TIME,
            cost=cost,
        )
        profile.balance -= cost
        profile.save()
        transaction.on_commit(lambda: current_app.send_task(
            "face2img:generate-image:task",
            kwargs=dict(
                pk=str(job.id),
            ),
        ))

    return job
