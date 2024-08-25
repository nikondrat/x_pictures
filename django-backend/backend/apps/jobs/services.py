import os
import io
import time
import uuid
import base64
import tempfile
from urllib.parse import urljoin
from urllib.request import urlretrieve, urlcleanup

import moviepy.editor as mp

import requests
from PIL import Image, ImageFilter
from novita_client.utils import image_to_base64

from django.conf import settings
from django.db import transaction
from django.core.files.base import File, ContentFile

from core.common import get_logger
from apps.jobs.utils import save_to_image_gallery, save_to_video_gallery
from apps.jobs.models import AbstractJob, UndressJob, GenerateJob, VideoJob

logger = get_logger('jobs:services')

JOBS: dict[str: AbstractJob] = {
    'undress': UndressJob,
    'generate': GenerateJob,
    'video': VideoJob,
}
WATERMARK = Image.open(settings.WATERMARK_IMAGE_PATH)

PIXELS_LIMIT = 1920 * 1080


def base64_to_image(image_b64_data: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(image_b64_data)))


def image_url_to_base64(image_url: str) -> str:
    return base64.b64encode(requests.get(image_url).content).decode('utf-8')


def set_watermark(image: Image.Image) -> Image.Image:
    position = ((image.width - WATERMARK.width), (image.height - WATERMARK.height))
    image.paste(WATERMARK, position, WATERMARK)
    return image


def blur_image(image: Image.Image) -> Image.Image:
    return image.copy().filter(ImageFilter.BoxBlur(5))


def _save_image(filename: str, field, image: Image.Image):
    buffer = io.BytesIO()
    image.save(buffer, 'jpeg')
    buffer.seek(0)
    field.save(filename, ContentFile(buffer.getvalue()), save=False)


@transaction.atomic()
def _make_image(image_b64_data: str, job: UndressJob | GenerateJob) -> UndressJob | GenerateJob:
    image = base64_to_image(image_b64_data=image_b64_data)

    if not job.need_watermark:
        _save_image(filename=f'{uuid.uuid4()}.jpeg', field=job.without_watermark_image, image=image)
    else:
        image = set_watermark(image=image)

    if job.need_blur:
        _save_image(filename=f'{uuid.uuid4()}.jpeg',
                    field=job.blur_image,
                    image=blur_image(image=image))

    _save_image(filename=f'{uuid.uuid4()}.jpeg', field=job.image, image=image)

    if isinstance(job, GenerateJob):
        save_to_image_gallery(job=job)

    return job


def set_watermark_to_video(inp_temp_filename, job: VideoJob):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    out_video_filename = tfp.name
    try:
        inp_video = mp.VideoFileClip(inp_temp_filename)

        # Create preview
        _save_image(
            filename=f'{uuid.uuid4()}.jpeg',
            field=job.preview,
            image=set_watermark(Image.fromarray(inp_video.get_frame(1)))
        )

        width, height = inp_video.size
        position = ((width - WATERMARK.width), (height - WATERMARK.height))

        logo = mp.ImageClip(
            str(settings.WATERMARK_IMAGE_PATH)
        ).set_position(
            position
        ).set_duration(
            inp_video.duration
        )

        video = mp.CompositeVideoClip([inp_video, logo])
        video.subclip(0).write_videofile(out_video_filename, codec='libx264')
        job.video.save(f'{uuid.uuid4()}.mp4', File(open(out_video_filename, 'rb')))
    except Exception as err:
        logger.error(f'Set watermark error: {err}')
        job.video.save(f'{uuid.uuid4()}.mp4', File(open(inp_temp_filename, 'rb')))
    finally:
        tfp.close()
        os.unlink(tfp.name)


@transaction.atomic()
def _make_video(video: str, job: VideoJob) -> VideoJob:
    if not video.startswith('http'):
        raise ValueError('Make video only url!')

    try:
        temp_video_filename, _ = urlretrieve(video)
        job.without_watermark_video.save(f'{uuid.uuid4()}.mp4', File(open(temp_video_filename, 'rb')))
        set_watermark_to_video(temp_video_filename, job=job)
    finally:
        urlcleanup()

    save_to_video_gallery(job=job)

    return job


def save_image_b64(image_b64: str, field):
    if len(image_b64.split(',')) > 1:
        _, image_data = image_b64.split(',')
    else:
        image_data = image_b64

    image = base64_to_image(image_b64_data=image_data)

    buffer = io.BytesIO()
    image.save(buffer, 'jpeg')
    buffer.seek(0)

    field.save(f'{uuid.uuid4()}.jpeg', ContentFile(buffer.getvalue()), save=True)
    return True


def rollback_balance(job: AbstractJob):
    if job.user:
        profile = job.user.profile
        profile.balance += job.cost
        profile.save()


@transaction.atomic()
def after_work_service(pk: str, job_type: str, result: dict):
    logger.info(f'Job ID: {pk}:: Job type: {job_type} :: Status: {result["status"]}')

    job = JOBS[job_type].objects.get(pk=pk)
    job.time_spent = result['time_spent']
    job.status = AbstractJob.Status(result['status'])

    if job.status == AbstractJob.Status.SUCCESS:
        if job_type == 'video':
            _make_video(video=result['video'], job=job)
        else:
            _make_image(image_b64_data=result['image'], job=job)
    else:
        job.show_in_profile = False
        rollback_balance(job=job)

    job.save()

    return True


def pillow_resize(width, height, flag: str):
    if flag == 'width':
        percent = 768 / width
        new_width = 768
        new_height = height * percent
    else:
        percent = 768 / height
        new_height = 768
        new_width = width * percent

    return int(new_width), int(new_height)


def get_correct_image_with_mask(image_b64: str, mask_b64: str):
    if len(image_b64.split(',')) > 1:
        _, image_data = image_b64.split(',')
    else:
        image_data = image_b64

    if len(mask_b64.split(',')) > 1:
        _, mask_data = mask_b64.split(',')
    else:
        mask_data = mask_b64

    image = base64_to_image(image_b64_data=image_data)
    mask = base64_to_image(image_b64_data=mask_data)

    width, height = image.size

    if width > 768 or height > 768:
        if width > height:
            flag = 'width'
        else:
            flag = 'height'
        width, height = pillow_resize(width=width, height=height, flag=flag)

    image = image.resize((width, height))
    mask = mask.resize((width, height)).convert('RGB')

    return (
        image_to_base64(image),
        image_to_base64(mask, format='png'),
        width, height
    )


class BuildMask:
    @classmethod
    def build(cls, image_b64: str):
        response = requests.post(settings.MASK_BUILDER_URL,
                                 json={
                                     'image_b64': image_b64,
                                     'code': settings.MASK_BUILDER_SECRET_CODE,
                                 })

        response.raise_for_status()
        response = response.json()
        return response['mask_b64']


class NovitaV3Provider:
    url = 'https://api.novita.ai/'

    def __init__(self, api_key: str):
        self._api_key = api_key

    def _create_task(self, payload: dict) -> str:
        response = requests.request(
            method='POST',
            url=urljoin(self.url, '/v3/async/txt2video'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._api_key}'
            },
            json=payload,
        )
        response.raise_for_status()
        return response.json()['task_id']

    def _get_task_result(self, task_id: str) -> dict:
        response = requests.request(
            method='GET',
            url=urljoin(self.url, '/v3/async/task-result'),
            headers={
                'Authorization': f'Bearer {self._api_key}'
            },
            params={
                'task_id': task_id,
            }
        )
        response.raise_for_status()
        return response.json()

    def get_task_result(self, task_id: str) -> dict:
        result = self._get_task_result(task_id=task_id)
        while result['task']['status'] != 'TASK_STATUS_SUCCEED':
            time.sleep(5)
            result = self._get_task_result(task_id=task_id)
            logger.info(f'Task: {task_id} :: Status: {result["task"]["status"]}')
        return result

    def sync__txt2video(self, model_name: str,
                        width: int, height: int,
                        steps: int, negative_prompt: str,
                        prompts: list[dict[int: str]],
                        guidance_scale: int) -> dict:
        task_id = self._create_task(
            payload={
                'extra': {
                    'response_video_type': 'mp4',
                },
                'model_name': model_name,
                'width': width,
                'height': height,
                'seed': -1,
                'steps': steps,
                'negative_prompt': negative_prompt,
                'prompts': prompts,
                'guidance_scale': guidance_scale,
                'loras': [{
                    'model_name': 'add_detail_44319',
                    'strength': 0.8,
                }],
                'embeddings': [],
                'clip_skip': 3,
            }
        )

        return self.get_task_result(task_id=task_id)
