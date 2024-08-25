import decimal
from typing import Optional

from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from core.common.cached.ram import Cached
from core.users.models import User
from apps.profiles.models import Profile, ProfileType
from apps.jobs.models import VideoJob
from apps.jobs.core.generate import Service as GenerateService

QUEUES = {
    3: 'vid_basic_queue',
    5: 'vid_advance_queue',
    8: 'vid_premium_queue',
    10: 'vid_super_premium_queue',
}

ESTIMATED_TIME = {
    ProfileType.basic: int(60 * 2.5),
    ProfileType.advance: int(60 * 2.5),
    ProfileType.premium: int(60 * 2.5),
    ProfileType.super_premium: int(60 * 2.5),
}


class Service(GenerateService):
    use_task = True
    task_name = 'jobs:create-video:task'

    @classmethod
    @Cached(timeout=60*15)
    def get_ml_params(cls, filter_ids: list[int], sd_model_id: Optional[int] = None,
                      action_id: Optional[int] = None) -> dict:
        params = super().get_ml_params(
            filter_ids=filter_ids,
            sd_model_id=sd_model_id,
            action_id=action_id,
        )

        params['prompt'] += ' (( color video ))'

        params.update({
            'guidance_scale': 7.5,
        })
        return params

    @classmethod
    def get_queue_by_priority(cls, priority: int) -> str:
        return QUEUES[priority]

    @classmethod
    def get_need_blur(cls, profile: Profile, cost: decimal.Decimal) -> bool:
        raise NotImplementedError()

    @classmethod
    def get_estimated_time(cls, profile: Profile) -> int:
        return ESTIMATED_TIME[profile.type]

    @classmethod
    def get_frames(cls, profile: Profile) -> int:
        return 63

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

        params = cls.get_ml_params(
            filter_ids=filter_ids,
            sd_model_id=kwargs['sd_model_id'],
            action_id=2,
        )

        estimated_time = cls.get_estimated_time(profile=profile)
        need_watermark = cls.get_need_watermark(profile=profile, cost=cost)
        priority = cls.get_priority(profile=profile)
        frames = cls.get_frames(profile=profile)

        job = VideoJob.objects.create(
            user_id=user_id,
            sd_model_id=kwargs['sd_model_id'],
            positive_prompt=params['prompt'],
            negative_prompt=params['negative_prompt'],
            step=params['step'],
            sampler_name=params['sampler_name'],
            estimated_time=estimated_time,
            status=VideoJob.Status.PROCESS,
            cost=cost,
            show_in_profile=True,
            need_watermark=need_watermark,
        )
        job.filters.add(*filter_ids)
        job.save()

        transaction.on_commit(lambda: cls.make_request(
            correlation_id=job.pk,
            data={
                'sd_model': job.sd_model.model_name,
                'size': cls.get_size(profile=profile),
                'next_queue': cls.get_queue_by_priority(priority=priority),
                'frames': frames,
                **params,
            },
            priority=priority,
        ))

        return job
