import decimal
from typing import Optional

from django.conf import settings
from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from core.users.models import User
from apps.jobs.models import UndressJob, Filter
from apps.jobs.core.base import BaseService

QUEUES = {
    1: 'und_free_queue',
    3: 'und_basic_queue',
    5: 'und_advance_queue',
    8: 'und_premium_queue',
    10: 'und_super_premium_queue',
}


class Service(BaseService):
    use_task = settings.USE_UNDRESS_NOVITA

    rabbitmq_queue = settings.ML_UNDRESS_QUEUE
    rabbitmq_routing_key = settings.ML_UNDRESS_QUEUE

    task_name = 'jobs:create-undress:task'

    @classmethod
    def get_ml_params(cls, filter_ids: list[int], sd_model_id: Optional[int] = None,
                      action_id: Optional[int] = None) -> dict:
        fil = Filter.objects.get(id=filter_ids[0])
        return {
            'prompt': fil.raw_prompt,
            'negative_prompt': fil.raw_negative_prompt,
            'step': 20,
            'sampler_name': 'DPM++ 2M SDE Karras',
        }

    @classmethod
    def get_queue_by_priority(cls, priority: int) -> str:
        return QUEUES[priority]

    @classmethod
    @transaction.atomic()
    def make_job(cls, user: User, filter_ids: list[int], cost: decimal.Decimal, **kwargs):
        profile = user_id = None
        if user.is_authenticated:
            user_id = user.pk
            profile = user.profile

        if profile and profile.balance >= cost:
            profile.balance -= cost
            profile.save()
        else:
            raise PermissionDenied('Not enough balance')

        params = cls.get_ml_params(filter_ids=filter_ids)
        estimated_time = cls.get_estimated_time(profile=profile)
        need_blur = cls.get_need_blur(profile=profile, cost=cost)
        need_watermark = cls.get_need_watermark(profile=profile, cost=cost)
        priority = cls.get_priority(profile=profile)

        job = UndressJob.objects.create(
            user_id=user_id,
            sd_model_id=1,
            action_id=1,
            positive_prompt=params['prompt'],
            negative_prompt=params['negative_prompt'],
            step=params['step'],
            sampler_name=params['sampler_name'],
            estimated_time=estimated_time,
            status=UndressJob.Status.PROCESS,
            cost=cost,
            show_in_profile=True,
            need_blur=need_blur,
            # need_watermark=need_watermark,
            need_watermark=False,
        )
        job.filters.add(*filter_ids)
        job.save()

        transaction.on_commit(lambda: cls.make_request(
            correlation_id=job.id,
            data={
                'image_b64': kwargs['image_b64'],
                'mask_b64': kwargs['mask_b64'],
                'sd_model': job.sd_model.model_name,
                'next_queue': cls.get_queue_by_priority(priority=priority),
                **params,
            },
            priority=priority,
        ))

        return job


class ServiceV2(Service):
    use_task = True
    task_name = 'jobs:create-undress-without-mask:task'

    @classmethod
    @transaction.atomic()
    def make_job(cls, user: User, filter_ids: list[int], cost: decimal.Decimal, **kwargs):
        profile = user_id = None
        if user.is_authenticated:
            user_id = user.pk
            profile = user.profile

        if profile and profile.balance >= cost:
            profile.balance -= cost
            profile.save()
        else:
            raise PermissionDenied('Not enough balance')

        params = cls.get_ml_params(filter_ids=filter_ids)
        estimated_time = cls.get_estimated_time(profile=profile)
        need_blur = cls.get_need_blur(profile=profile, cost=cost)
        need_watermark = cls.get_need_watermark(profile=profile, cost=cost)
        priority = cls.get_priority(profile=profile)

        job = UndressJob.objects.create(
            user_id=user_id,
            sd_model_id=1,
            action_id=1,
            positive_prompt=params['prompt'],
            negative_prompt=params['negative_prompt'],
            step=params['step'],
            sampler_name=params['sampler_name'],
            estimated_time=estimated_time,
            status=UndressJob.Status.PROCESS,
            cost=cost,
            show_in_profile=True,
            need_blur=need_blur,
            # need_watermark=need_watermark,
            need_watermark=False,
        )
        job.filters.add(*filter_ids)

        queue = cls.get_queue_by_priority(priority=priority)

        transaction.on_commit(lambda: cls.make_request(
            correlation_id=job.id,
            data={
                'image_b64': kwargs['image_b64'],
                'sd_model': job.sd_model.model_name,
                'next_queue': queue,
                **params,
            },
            priority=priority,
        ))

        job.save()

        return job
