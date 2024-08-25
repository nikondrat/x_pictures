from __future__ import annotations

from typing import Any, Type
from datetime import timedelta
from urllib.parse import urljoin

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from apps.mailing.models import Message, Event


def get_event(message: Message) -> Type[BaseEvent]:
    if message.event == Event.first_event_2024:
        return FirstEvent2024


class BaseEvent:
    model = Message
    event: Event
    lifetime: timedelta

    template: str

    @classmethod
    def get_link(cls, message: Message) -> str: ...

    @classmethod
    def make_message(cls, message: Message): ...

    @classmethod
    def handler(cls, secret_code: str, **kwargs) -> Any: ...


class FirstEvent2024(BaseEvent):
    event = Event.first_event_2024
    template = 'messages/first_event_2024.html'
    redirect_url = ('https://x-pictures.io/aiporn?utm_source=own&utm_medium='
                    'email&utm_campaign=promo&utm_content=freetokens')

    lifetime = timedelta(days=3)

    @classmethod
    def get_link(cls, message: Message) -> str:
        path = reverse('mailing:first_event_2024', kwargs={'secret_code': message.secret_code})
        return urljoin(settings.DOMAIN, path)

    @classmethod
    def make_message(cls, message: Message):
        html_message = render_to_string(cls.template, {
            'message': message,
            'link': cls.get_link(message=message),
        })

        return (
            _('Unlock New Features with Your Free Tokens at X-pictures!'),
            html_message,
            strip_tags(html_message),
        )

    @classmethod
    @transaction.atomic()
    def handler(cls, secret_code: str, **kwargs) -> str:
        message: Message = Message.objects.filter(secret_code=secret_code, event=cls.event).first()
        if not message:
            return cls.redirect_url

        if message.status != Message.Status.SENT:
            return cls.redirect_url

        if message.is_expired:
            message.status = Message.Status.EXPIRED
            message.save()
            return cls.redirect_url

        profile = message.user.profile
        if profile.balance < 2:
            profile.balance = 2
            profile.save()

        message.status = Message.Status.SUCCESS
        message.save()
        return cls.redirect_url
