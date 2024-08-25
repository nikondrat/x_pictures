import io
import time
import base64
from datetime import timedelta

from celery import shared_task, current_app
from django.conf import settings
from django.utils import timezone

from novita_client import NovitaClient, Txt2ImgRequest, Img2ImgRequest

from core.common.utils import get_logger
from apps.jobs.models import UndressJob, GenerateJob, InstagramUndressJob, VideoJob
from apps.jobs.models import ImageGallery, VideoGallery
from apps.jobs.services import BuildMask, NovitaV3Provider
from apps.jobs.services import after_work_service, get_correct_image_with_mask, image_url_to_base64, save_image_b64

logger = get_logger('jobs:tasks')


@shared_task(name='jobs:close-timeout-jobs:task')
def close_timeout_jobs_task():
    # Undress job
    UndressJob.objects.filter(
        status__in=[UndressJob.Status.CREATED, UndressJob.Status.PROCESS],
        updated__lte=timezone.now() - timedelta(minutes=10),
    ).update(status=UndressJob.Status.ERROR, show_in_profile=False)
    # Generate job
    GenerateJob.objects.filter(
        status__in=[GenerateJob.Status.CREATED, GenerateJob.Status.PROCESS],
        updated__lte=timezone.now() - timedelta(minutes=10),
    ).update(status=GenerateJob.Status.ERROR, show_in_profile=False)
    # Instagram undress job
    InstagramUndressJob.objects.filter(
        status__in=[InstagramUndressJob.Status.CREATED, InstagramUndressJob.Status.PROCESS],
        detail_status=InstagramUndressJob.DetailStatus.PROCESS_PARSER,
        updated__lte=timezone.now() - timedelta(minutes=20),
    ).update(status=InstagramUndressJob.Status.ERROR,
             detail_status=InstagramUndressJob.DetailStatus.EXPIRED_PARSER)
    InstagramUndressJob.objects.filter(
        status__in=[InstagramUndressJob.Status.CREATED, InstagramUndressJob.Status.PROCESS],
        detail_status=InstagramUndressJob.DetailStatus.PROCESS_MAKE_MASK,
        updated__lte=timezone.now() - timedelta(minutes=20),
    ).update(status=InstagramUndressJob.Status.ERROR,
             detail_status=InstagramUndressJob.DetailStatus.EXPIRED_MAKE_MASK)
    InstagramUndressJob.objects.filter(
        status__in=[InstagramUndressJob.Status.CREATED, InstagramUndressJob.Status.PROCESS],
        detail_status=InstagramUndressJob.DetailStatus.PROCESS_JOB,
        updated__lte=timezone.now() - timedelta(minutes=20),
    ).update(status=InstagramUndressJob.Status.ERROR,
             detail_status=InstagramUndressJob.DetailStatus.EXPIRED_JOB)
    # Video job
    VideoJob.objects.filter(
        status__in=[GenerateJob.Status.CREATED, GenerateJob.Status.PROCESS],
        updated__lte=timezone.now() - timedelta(minutes=15),
    ).update(status=GenerateJob.Status.ERROR, show_in_profile=False)


@shared_task(name='jobs:delete-blur-images:task')
def delete_blur_images_task():
    # TODO доделать и найти как тестить
    for job in GenerateJob.objects.exclude(
            blur_image__isnull=True,
    ).filter(
        need_blur=True,
        status=UndressJob.Status.SUCCESS,
        updated__lte=timezone.now() - timedelta(days=7),
    ):
        job.blur_image.delete(save=False)


@shared_task(name='jobs:delete-undress-images:task')
def delete_undress_images_task():
    # TODO доделать и найти как тестить
    for job in UndressJob.objects.filter(
            need_blur=True,
            status=UndressJob.Status.SUCCESS,
            updated__lte=timezone.now() - timedelta(days=7),
    ):
        if job.blur_image:
            job.blur_image.delete(save=False)
        if job.image:
            job.image.delete(save=False)
        if job.without_watermark_image:
            job.without_watermark_image.delete(save=False)
        job.show_in_profile = False
        job.save()


@shared_task(name='jobs:create-generate:task')
def create_generate_task(pk: str, data: dict):
    client = NovitaClient(settings.NOVITA_CLIENT_API_KEY)
    next_queue = data.pop('next_queue', 'celery')

    try:
        width, height = data['size']
        start = time.time()
        res = client.sync_txt2img(Txt2ImgRequest(
            model_name=data['sd_model'],
            prompt=data['prompt'],
            negative_prompt=data['negative_prompt'],
            steps=data['step'],
            width=width,
            height=height,
            sampler_name=data['sampler_name'],
            cfg_scale=7,
            batch_size=1,
            n_iter=1,
            seed=-1
        )).data.imgs_bytes
        time_spent = time.time() - start
        result = {
            'image': base64.b64encode(io.BytesIO(res[0]).getvalue()).decode('utf-8'),
            'status': 2,
            'time_spent': int(time_spent),
        }
        logger.info(f'Generate: {pk} :: Success')
    except Exception as err:
        logger.error(f'Generate: {pk} :: Error: {err}')
        result = {
            'status': -1,
            'time_spent': 0,
        }

    return current_app.send_task(
        'jobs:after-work:task',
        kwargs={
            'pk': pk,
            'job_type': 'generate',
            'result': result,
        },
        queue=next_queue,
    )


@shared_task(name='jobs:create-undress:task')
def create_undress_task(pk: str, data: dict):
    client = NovitaClient(settings.NOVITA_CLIENT_API_KEY)
    next_queue = data.pop('next_queue', 'celery')

    try:
        correct_image, correct_mask, width, height = get_correct_image_with_mask(
            image_b64=data['image_b64'],
            mask_b64=data['mask_b64'],
        )
        start = time.time()
        res = client.sync_img2img(Img2ImgRequest(
            model_name=data['sd_model'],
            sampler_name=data['sampler_name'],
            init_images=[correct_image],
            mask=correct_mask,
            prompt=data['prompt'],
            negative_prompt=data['negative_prompt'],
            steps=data['step'],
            width=width,
            height=height,
            resize_mode=0,
            cfg_scale=7,
            batch_size=1,
            mask_blur=0,
            n_iter=1,
            inpaint_full_res=1,
            inpaint_full_res_padding=45,
            inpainting_mask_invert=0,
            denoising_strength=0.9,
            inpainting_fill=0,
            seed=-1,
        )).data.imgs_bytes

        time_spent = time.time() - start
        result = {
            'image': base64.b64encode(io.BytesIO(res[0]).getvalue()).decode('utf-8'),
            'status': 2,
            'time_spent': int(time_spent),
        }
        logger.info(f'Undress: {pk} :: Success')
    except Exception as err:
        logger.error(f'Undress: {pk} :: Error: {err}')
        result = {
            'status': -1,
            'time_spent': 0,
        }

    return current_app.send_task(
        'jobs:after-work:task',
        kwargs={
            'pk': pk,
            'job_type': 'undress',
            'result': result,
        },
        queue=next_queue,
    )


@shared_task(name='jobs:create-undress-without-mask:task')
def create_undress_without_mask_task(pk: str, data: dict):
    next_queue = data.pop('next_queue')
    try:
        mask_b64 = BuildMask.build(image_b64=data['image_b64'])
    except Exception as err:
        logger.error(f'Undress without mask {pk} :: Error: {err}')
        return current_app.send_task(
            'jobs:after-work:task',
            kwargs={
                'pk': pk,
                'job_type': 'undress',
                'result': {
                    'status': -1,
                    'time_spent': 0,
                },
            },
        )

    data.update({
        'mask_b64': mask_b64,
        'next_queue': next_queue,
    })

    return current_app.send_task(
        'jobs:create-undress:task',
        kwargs={
            'pk': pk,
            'data': data,
        },
        queue=next_queue,
    )


@shared_task(name='jobs:after-work:task')
def after_work_task(pk: str, job_type: str, result: dict):
    return after_work_service(pk=pk, job_type=job_type, result=result)


@shared_task(name='jobs:close-success-inst-jobs:task')
def close_success_inst_jobs():
    for job in InstagramUndressJob.objects.filter(
            status=InstagramUndressJob.Status.PROCESS,
            detail_status=InstagramUndressJob.DetailStatus.PROCESS_JOB,
    ):
        if job.jobs.filter(status=UndressJob.Status.PROCESS).exists():
            continue

        job.status = InstagramUndressJob.Status.SUCCESS
        job.detail_status = InstagramUndressJob.DetailStatus.SUCCESS_JOB
        job.save()

    return True


@shared_task(name='jobs:inst-parser-control:task')
def inst_parser_control_task(pk: str):
    from apps.jobs.core import InstagramUndressService
    job = InstagramUndressJob.objects.get(pk=pk)

    count = 0
    while True:
        if count >= 155:
            job.status = InstagramUndressJob.Status.ERROR
            job.detail_status = InstagramUndressJob.DetailStatus.EXPIRED_PARSER
            job.save()
            return False

        job = InstagramUndressService.check_step1(user=job.user, job=job)
        if not job.is_parsing:
            break
        count += 1
        time.sleep(2)

    return True


@shared_task(name='jobs:inst-make-make:task')
def inst_make_make_task(pk: str):
    job = InstagramUndressJob.objects.get(pk=pk)

    for source in job.sources.all():
        image_b64 = image_url_to_base64(image_url=source.image_url)
        try:
            mask_b64 = BuildMask.build(image_b64=image_b64)
            save_image_b64(mask_b64, field=source.basic_mask)
        except Exception as err:
            logger.error(f'Undress without mask {pk} :: Error: {err}')
            continue

    job.detail_status = InstagramUndressJob.DetailStatus.SUCCESS_MAKE_MASK
    job.save()

    return True


@shared_task(name='jobs:inst-undress-proxy:task')
def inst_undress_proxy_task(pk: str, data: dict, image_url: str, mask_url: str = None):
    data.update({
        'image_b64': image_url_to_base64(image_url=image_url),
    })
    if mask_url:
        data.update({
            'mask_b64': image_url_to_base64(image_url=mask_url),
        })

    return current_app.send_task(
        'jobs:create-undress:task',
        kwargs={
            'pk': pk,
            'data': data,
        },
        queue=data['next_queue'],
    )


@shared_task(name='jobs:create-video:task')
def create_video_task(pk: str, data: dict):
    next_queue = data.pop('next_queue', 'celery')
    provider = NovitaV3Provider(settings.NOVITA_CLIENT_API_KEY)

    try:
        width, height = data['size']
        start = time.time()
        result = provider.sync__txt2video(
            model_name=data['sd_model'],
            steps=data['step'],
            negative_prompt=data['negative_prompt'],
            prompts=[{
                'frames': data['frames'],
                'prompt': data['prompt'],
            }],
            width=width, height=height,
            guidance_scale=data['guidance_scale'],
        )
        time_spent = time.time() - start

        result = {
            'video': result['videos'][0]['video_url'],
            'status': 2,
            'time_spent': int(time_spent),
        }
        logger.info(f'Video: {pk} :: Success :: {result["video"]}')
    except Exception as err:
        logger.error(f'Video: {pk} :: Error: {err}')
        result = {
            'status': -1,
            'time_spent': 0,
        }

    return current_app.send_task(
        'jobs:after-work:task',
        kwargs={
            'pk': pk,
            'job_type': 'video',
            'result': result,
        },
        queue=next_queue,
    )


@shared_task(name='jobs:add-to-gallery:task')
def add_to_gallery_task(gallery_type: str, job_pk: str):
    if gallery_type == 'image':
        job = GenerateJob.objects.get(pk=job_pk)
        if job.sd_model_id != 12:
            ImageGallery.objects.create(
                job=job,
            )
    else:
        job = VideoJob.objects.get(pk=job_pk)
        VideoGallery.objects.create(
            job=job,
        )

    return True
