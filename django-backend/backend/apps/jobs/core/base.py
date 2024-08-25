import abc
import uuid
import json
import decimal
from typing import Optional

import pika
from celery import current_app

from django.conf import settings

from core.users.utils import User
from apps.profiles.models import Profile, ProfileType

ESTIMATED_TIME = {
    ProfileType.basic: int(60 * 1.5),
    ProfileType.advance: int(60 * 1),
    ProfileType.premium: int(60 * 0.5),
    ProfileType.super_premium: int(60 * 0.5),
}

PRIORITY = {
    ProfileType.basic: 3,
    ProfileType.advance: 5,
    ProfileType.premium: 8,
    ProfileType.super_premium: 10,
}


class BaseService:
    use_task: bool

    rabbitmq_url: str = settings.RABBITMQ_URL
    rabbitmq_queue: str
    rabbitmq_routing_key: str
    rabbitmq_reply_to: str = settings.ML_CALLBACK_QUEUE

    task_name: str

    @classmethod
    def get_need_blur(cls, profile: Profile, cost: decimal.Decimal) -> bool:
        return profile is None or profile.balance < cost

    @classmethod
    def get_need_watermark(cls, profile: Profile, cost: decimal.Decimal) -> bool:
        return (
                not profile or
                profile.type not in (ProfileType.premium, ProfileType.super_premium) or
                profile.balance < cost
        )

    @classmethod
    def get_estimated_time(cls, profile: Profile) -> int:
        if profile:
            return ESTIMATED_TIME[profile.type]
        return 60

    @classmethod
    def get_priority(cls, profile: Profile) -> int:
        if profile:
            return PRIORITY[profile.type]
        return 1

    @classmethod
    def get_size(cls, profile: Profile) -> tuple[int, int]:
        return 570, 768

    @classmethod
    def call_rabbitmq(cls, correlation_id: uuid.UUID, data: dict, priority: int):
        with pika.BlockingConnection(pika.URLParameters(cls.rabbitmq_url)) as connection:
            with connection.channel() as channel:
                channel.queue_declare(
                    queue=cls.rabbitmq_queue,
                    durable=True,
                    arguments={'x-max-priority': 10},
                )
                channel.basic_publish(
                    exchange='',
                    routing_key=cls.rabbitmq_routing_key,
                    body=json.dumps(data).encode(),
                    properties=pika.BasicProperties(
                        correlation_id=str(correlation_id),
                        priority=priority,
                        reply_to=cls.rabbitmq_reply_to,
                    )
                )

    @classmethod
    def call_task(cls, correlation_id: uuid.UUID, data: dict, priority: int):
        current_app.send_task(
            cls.task_name,
            kwargs={
                'pk': correlation_id,
                'data': data,
            },
            queue=cls.get_queue_by_priority(priority=priority)
        )

    @classmethod
    def make_request(cls, correlation_id: uuid.UUID, data: dict, priority: int):
        if cls.use_task:
            return cls.call_task(
                correlation_id=correlation_id,
                data=data,
                priority=priority,
            )
        else:
            return cls.call_rabbitmq(
                correlation_id=correlation_id,
                data=data,
                priority=priority,
            )

    @classmethod
    @abc.abstractmethod
    def get_ml_params(cls, filter_ids: list[int], sd_model_id: Optional[int] = None,
                      action_id: Optional[int] = None) -> dict:
        ...

    @classmethod
    @abc.abstractmethod
    def get_queue_by_priority(cls, priority: int) -> str:
        ...

    @classmethod
    @abc.abstractmethod
    def make_job(cls, user: User, filter_ids: list[int], cost: decimal.Decimal, **kwargs):
        ...
