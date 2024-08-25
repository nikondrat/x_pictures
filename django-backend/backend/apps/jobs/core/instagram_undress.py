import decimal
from urllib.parse import urljoin

import requests
from celery import current_app
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException

from core.users.models import User
from apps.profiles.models import Profile, ProfileType
from apps.jobs.models import UndressJob, InstagramUndressJob, InstagramSource

from apps.jobs.core import UndressService

LINK_TYPE = {
    'account': InstagramUndressJob.LinkType.account,
    'image': InstagramUndressJob.LinkType.photo,
}

QUEUES = {
    ProfileType.basic: 'inst_basic_queue',
    ProfileType.advance: 'inst_advance_queue',
    ProfileType.premium: 'inst_premium_queue',
    ProfileType.super_premium: 'inst_super_premium_queue',
}


class Service:
    base_url = settings.INSTAGRAM_PARSER_URL
    scode = settings.INSTAGRAM_PARSER_SCODE

    task_name_parser = 'jobs:inst-parser-control:task'
    task_name_make_mask = 'jobs:inst-make-make:task'
    task_name_proxy_undress = 'jobs:inst-undress-proxy:task'

    @classmethod
    @transaction.atomic()
    def rollback_balance(cls, profile: Profile, cost: decimal.Decimal):
        profile.balance += cost
        profile.save()

    @classmethod
    def get_parser_estimated_time(cls, profile: Profile):
        return int(180)

    @classmethod
    def get_queue_by_profile_type(cls, profile_type: ProfileType) -> str:
        return QUEUES[profile_type]

    @classmethod
    def get_link_type(cls, link: str) -> InstagramUndressJob.LinkType:
        response = requests.get(
            urljoin(cls.base_url, '/check_url'),
            params={
                'link_or_username': link,
                'scode': cls.scode,
            }
        )
        if not response.ok or not response.json()['status']:
            raise ValidationError({
                'link': _('Incorrect link'),
            })

        response = response.json()

        return LINK_TYPE[response['type']]

    @classmethod
    @transaction.atomic()
    def create_step1(cls, user: User, link: str, cost: decimal.Decimal, qty: int = 12) -> InstagramUndressJob:
        profile = user.profile
        if profile.balance - cost < decimal.Decimal('0'):
            raise ValidationError({
                'balance': _('Not enough balance!'),
            })

        link_type = cls.get_link_type(link=link)

        response = requests.post(
            urljoin(cls.base_url, '/task'),
            json={
                'link_or_username': link,
                'scode': cls.scode,
                'qty': qty,
            },
        )

        if not response.ok or not response.json()['status']:
            raise APIException({
                '__all__': _('Instagram parser error'),
            })

        profile.balance -= cost
        profile.save()

        job = InstagramUndressJob.objects.create(
            id=response.json()['task_id'],
            user_id=user.pk,
            status=InstagramUndressJob.Status.PROCESS,
            detail_status=InstagramUndressJob.DetailStatus.PROCESS_PARSER,
            link=link,
            link_type=link_type,
            parser_estimated_time=cls.get_parser_estimated_time(profile=profile),
        )
        transaction.on_commit(lambda: current_app.send_task(
            cls.task_name_parser,
            kwargs=dict(
                pk=str(job.id),
            ),
            queue=cls.get_queue_by_profile_type(profile_type=user.profile.type),
        ))

        return job

    @classmethod
    @transaction.atomic()
    def check_step1(cls, user: User, job: InstagramUndressJob):
        if job.is_make_mask:
            return job

        response = requests.get(
            urljoin(cls.base_url, '/task'),
            params={
                'task_id': str(job.id),
                'scode': cls.scode,
            }
        )

        if response.status_code == status.HTTP_404_NOT_FOUND:
            job.status = InstagramUndressJob.Status.ERROR
            job.detail_status = InstagramUndressJob.DetailStatus.ERROR_PARSER
            job.save()
            return job

        if not response.ok:
            return job

        if response.json()['status'] in (0, 1):
            for image_url in response.json()['links']:
                if not job.sources.filter(image_url=image_url).exists():
                    job.sources.create(
                        image_url=image_url,
                    )
            return job

        img_count = job.sources.count()

        if response.json()['status'] == -1 and img_count == 0:
            job.status = InstagramUndressJob.Status.ERROR
            job.detail_status = InstagramUndressJob.DetailStatus.ERROR_PARSER
            cls.rollback_balance(profile=user.profile,
                                 cost=decimal.Decimal('0.3'))
            job.save()
        elif response.json()['status'] == -2 and img_count == 0:
            job.status = InstagramUndressJob.Status.ERROR
            job.detail_status = InstagramUndressJob.DetailStatus.EXPIRED_PARSER
            cls.rollback_balance(profile=user.profile,
                                 cost=decimal.Decimal('0.3'))
            job.save()
        else:
            job.detail_status = InstagramUndressJob.DetailStatus.PROCESS_MAKE_MASK
            for image_url in response.json()['links']:
                if not job.sources.filter(image_url=image_url).exists():
                    job.sources.create(
                        image_url=image_url,
                    )
            job.save()

            transaction.on_commit(lambda: current_app.send_task(
                cls.task_name_make_mask,
                kwargs=dict(
                    pk=str(job.id),
                ),
                queue=cls.get_queue_by_profile_type(profile_type=user.profile.type),
            ))
        return job

    @classmethod
    def _make_single_undress_job(cls, job: InstagramUndressJob, source: InstagramSource,
                                 filter_ids: list, params: dict, estimated_time: int, need_blur: bool,
                                 need_watermark: bool, cost: decimal.Decimal,
                                 queue: str, undress_queue: str, custom_masks: dict) -> UndressJob:
        sub_job = UndressJob.objects.create(
            user_id=job.user_id,
            sd_model_id=1,
            action_id=1,
            positive_prompt=params['prompt'],
            negative_prompt=params['negative_prompt'],
            step=params['step'],
            sampler_name=params['sampler_name'],
            estimated_time=estimated_time,
            status=UndressJob.Status.PROCESS,
            cost=cost,
            show_in_profile=False,
            need_blur=need_blur,
            need_watermark=need_watermark,
        )
        sub_job.filters.add(*filter_ids)
        job.jobs.add(sub_job.pk)

        data = {
            'next_queue': undress_queue,
            'sd_model': sub_job.sd_model.model_name,
            **params,
        }

        kwargs = {
            'pk': str(sub_job.pk),
            'image_url': source.image_url,
            'mask_url': None,
            'data': data,
        }
        if mask_b64 := custom_masks.get(source.id):
            data.update({
                'mask_b64': mask_b64,
            })
        elif source.basic_mask is not None:
            kwargs.update({
                'mask_url': source.basic_mask.url,
            })
        else:
            return

        transaction.on_commit(lambda: current_app.send_task(
            cls.task_name_proxy_undress,
            kwargs=kwargs,
            queue=queue,
        ))
        return sub_job

    @classmethod
    @transaction.atomic()
    def create_step2(cls, user: User, job: InstagramUndressJob, cost: decimal.Decimal,
                     filter_ids: dict, exclude_ids: list[int],
                     custom_masks: dict[int: str]) -> InstagramUndressJob:
        profile = user.profile
        sources = job.sources.exclude(pk__in=exclude_ids)
        total_cost = sources.count() * cost
        if profile.balance - total_cost < decimal.Decimal('0'):
            raise ValidationError({
                'balance': _('Not enough balance!'),
            })

        estimated_time = UndressService.get_estimated_time(profile=profile)
        need_blur = UndressService.get_need_blur(profile=profile, cost=cost)
        need_watermark = UndressService.get_need_watermark(profile=profile, cost=cost)
        priority = UndressService.get_priority(profile=profile)

        queue = cls.get_queue_by_profile_type(profile_type=profile.type)
        undress_queue = UndressService.get_queue_by_priority(priority=priority)

        profile.balance -= total_cost
        profile.save()

        for source in sources:
            source_filter_ids = filter_ids.get(source.pk, [1])
            params = UndressService.get_ml_params(filter_ids=source_filter_ids)
            cls._make_single_undress_job(
                job=job, source=source,
                filter_ids=source_filter_ids, params=params,
                estimated_time=estimated_time, need_blur=need_blur,
                need_watermark=need_watermark, cost=cost, queue=queue,
                undress_queue=undress_queue, custom_masks=custom_masks,
            )

        job.detail_status = InstagramUndressJob.DetailStatus.PROCESS_JOB
        job.save()

        return job
