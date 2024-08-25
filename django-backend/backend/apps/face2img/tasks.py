import io
import time
import uuid
from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django.core.files.base import ContentFile
from PIL import Image
from django.conf import settings
from novita_client import NovitaClient, FACE_TRAINING_DEFAULT_COMPONENTS, Txt2ImgRequest, ADEtailer

from core.common.utils import get_logger
from apps.face2img.models import Lora, Face2ImgJob, Face2ImgJobResult

logger = get_logger('face2img:tasks')

LORA_TRAINING_BASE_MODEL = 'epicrealism_naturalSin_121250'
LORA_TRAINING_INSTANCE_PROMPT = "a closeup photo of ohwx person"
FIRST_STAGE_LORA_SCALE = 0.5
SECOND_STAGE_LORA_SCALE = 1.0
SECOND_STAGE_STRENGTH = 0.55


@shared_task(name='face2img:close-timeout-jobs:task')
def close_timeout_jobs_task():
    # Lora job
    Lora.objects.filter(
        status__in=[Lora.Status.CREATED, Lora.Status.PROCESS],
        updated__lte=timezone.now() - timedelta(minutes=60),
    ).update(status=Lora.Status.ERROR)

    # Face2Img job
    Face2ImgJob.objects.filter(
        status__in=[Face2ImgJob.Status.CREATED, Face2ImgJob.Status.PROCESS],
        updated__lte=timezone.now() - timedelta(minutes=10),
    ).update(status=Face2ImgJob.Status.ERROR)


def get_image_for_training(lora: Lora) -> list[Image]:
    results = []
    for training_face in lora.training_faces.all():
        results.append(Image.open(training_face.image))
    return results


@shared_task(name='face2img:training-lora:task')
def training_lora_task(pk: str):
    lora = Lora.objects.select_related("training_faces").get(pk=pk)
    images = get_image_for_training(lora=lora)

    client = NovitaClient(settings.NOVITA_CLIENT_API_KEY)

    train_task_id = client.create_training_subject(
        name=lora.lora_name,
        base_model=LORA_TRAINING_BASE_MODEL,
        images=images,
        instance_prompt=LORA_TRAINING_INSTANCE_PROMPT,
        class_prompt="person",
        max_train_steps="2000",
        components=FACE_TRAINING_DEFAULT_COMPONENTS,
        learning_rate=str(3e-4),
        seed=None,
        lr_scheduler='cosine_with_restarts',
        with_prior_preservation=True,
        prior_loss_weight=1.0,
        width=512,
        height=512,
        lora_r=32,
        lora_alpha=32,
        lora_text_encoder_r=32,
        lora_text_encoder_alpha=32
    )

    lora.train_task_id = train_task_id
    lora.save()

    train_model_name = None
    try:
        start = time.time()
        while True:
            train_task_status = client.query_training_subject_status(task_id=train_task_id)
            if train_task_status.task_status == "TRAINING" or train_task_status.task_status == "QUEUING":
                print("Training in progress...")
                time.sleep(30)
            elif train_task_status.task_status == "SUCCESS":
                train_model_name = train_task_status.models[0].model_name
                print(f"Training completed successfully! Model id: {train_task_status.models[0].model_name}")
                break
            elif train_task_status.task_status == "FAILED":
                print("Training failed!")
                break
            else:
                print(f"Unknown training status: {train_task_status.task_status}")
                break
    except Exception as err:
        logger.error(f'Lora: {pk} :: Error: {err}')
        lora.status = Lora.Status.ERROR
        lora.save()
        return False

    time_spent = time.time() - start
    if not train_model_name:
        lora.status = Lora.Status.ERROR
        lora.save()
        return False

    train_model_name = train_model_name.replace(".safetensors", "")
    lora.train_model_name = train_model_name
    lora.status = Lora.Status.SUCCESS
    lora.training_time_seconds = time_spent
    lora.save()
    return True


@shared_task(name='face2img:generate-image:task')
def generate_images_task(pk: str):
    job = Face2ImgJob.objects.select_related("pack", "lora").get(pk=pk)

    client = NovitaClient(settings.NOVITA_CLIENT_API_KEY)

    prompt = job.pack.positive_prompt.format(
        lora=f"<lora:{job.lora.train_model_name}:{FIRST_STAGE_LORA_SCALE}>"
    )

    lora_for_adetailer_prompt = f"<lora:{job.lora.train_model_name}:{SECOND_STAGE_LORA_SCALE}>"
    adetailer_prompt = f"a closeup photo of ohwx person, masterpiece, {lora_for_adetailer_prompt}"
    request = Txt2ImgRequest(
        prompt=prompt,
        negative_prompt=job.pack.negative_prompt,
        sampler_name=job.pack.sampler_name,
        model_name=job.pack.sd_model,
        height=job.pack.image_default_height,
        width=job.pack.image_default_width,
        steps=job.pack.steps,
        batch_size=job.pack.batch_size,
        adetailer=ADEtailer(
            prompt=adetailer_prompt,
            steps=20,
            strength=SECOND_STAGE_STRENGTH,
        )
    )

    try:
        start = time.time()
        response = client.sync_txt2img(request=request)
        time_spent = time.time() - start
    except Exception as err:
        logger.error(f'Face2Img: {pk} :: Error: {err}')
        job.status = Face2ImgJob.Status.ERROR
        job.save()
        return True

    images = []
    for img_bytes in response.data.imgs_bytes:
        images.append(Image.open(io.BytesIO(img_bytes)))

    for image in images:
        try:
            result = Face2ImgJobResult.objects.create(
                job=job,
            )
            buffer = io.BytesIO()
            image.save(buffer, 'jpeg')
            buffer.seek(0)
            result.image.save(f"{uuid.uuid4()}.jpeg", ContentFile(buffer.getvalue()), save=False)
        except Exception as err:
            logger.error(f'Face2Img: {pk} :: Error: {err}')

    job.status = Face2ImgJob.Status.SUCCESS
    job.time_spent = time_spent
    job.save()

    return True
