import uuid
from typing import Optional

from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

from core.users import models
from core.users import config
from core.users.services import send_email
from core.users.utils import get_user_by_email


def create_token(user_id: str) -> models.Token:
    token = models.Token.objects.create(user_id=user_id)
    models.Token.expired_qs().delete()
    return token


def is_unique_account(ip_address: Optional[str] = None) -> bool:
    if ip_address:
        return not models.User.objects.filter(ip_address=ip_address).exists()
    return True


@transaction.atomic()
def registration_user(email: str, password: str,
                      auth_provider: models.User.AuthProvider = models.User.AuthProvider.email,
                      click_id: Optional[str] = None,
                      ip_address: Optional[str] = None,
                      use_verification: bool = True) -> tuple:
    from apps.profiles.models import Profile

    user = models.User.objects.create(
        id=models.generate_user_id(),
        email=email,
        decoded_password=password,
        auth_provider=auth_provider,
        ip_address=ip_address,
        is_unique_account=is_unique_account(ip_address=ip_address),
    )
    user.set_password(raw_password=password)
    user.save()

    start_balance = 0
    if user.is_unique_account:
        start_balance = config.AFTER_REGISTRATION_TOKEN

    Profile.objects.create(
        owner=user,
        balance=start_balance,
    )

    # Reg AlanBase account
    models.AlanBase.objects.create(user=user, click_id=click_id)

    if use_verification:
        send_email(user_id=user.pk, email=user.email,
                   typ=models.EmailMessage.MessageType.verification)
    else:
        user.email_confirmed = True
        add_token_after_verification(user=user)
        user.save()

    token = create_token(user_id=user.pk)

    return user, token


@transaction.atomic()
def login_user(user: models.User):
    return create_token(user_id=user.pk)


def add_token_after_verification(user: models.User):
    if user.is_unique_account:
        user.profile.balance += config.AFTER_VERIFICATION_TOKEN
        user.profile.save()


@transaction.atomic()
def verification_user(token: str):
    message = models.EmailMessage.objects.filter(
        pk=token, status=models.EmailMessage.Status.SENT,
        type=models.EmailMessage.MessageType.verification,
    ).first()
    if message:
        message.status = models.EmailMessage.Status.SUCCESS
        user = message.user
        user.email_confirmed = True

        add_token_after_verification(user=user)

        message.save()
        user.save()


@transaction.atomic()
def password_reset(user: models.User, new_password: str, token: str):
    models.EmailMessage.objects.filter(user_id=user.pk, key=token).update(
        status=models.EmailMessage.Status.SUCCESS,
    )
    user.decoded_password = new_password
    user.password = make_password(new_password)
    user.save()


@transaction.atomic()
def social_media_auth(email: str, auth_provider: models.User.AuthProvider,
                      ip_address: Optional[str] = None, click_id: Optional[str] = None):
    if auth_provider == models.User.AuthProvider.google:
        user = get_user_by_email(email=email)
        if not user:
            user, token = registration_user(
                email=email,
                password=settings.SOCIAL_SECRET,
                auth_provider=models.User.AuthProvider.google,
                click_id=click_id,
                ip_address=ip_address,
                use_verification=False,
            )
            return user, token, True
        if not user.click_id and click_id:
            try:
                alanbase, _ = models.AlanBase.objects.get_or_create(user=user)
                alanbase.click_id = click_id
                alanbase.save()
            except Exception:
                pass

        return user, login_user(user=user), False
    raise ValidationError({
        'email': _('The account was registered in a different way')
    })


@transaction.atomic()
def add_job_after_registration(user: models.User, **kwargs):
    if kwargs.get('generate_job_id'):
        from apps.jobs.models import GenerateJob
        job: GenerateJob = GenerateJob.objects.filter(pk=uuid.UUID(kwargs['generate_job_id'])).first()
        if not job:
            return

        if job.user_id is None:
            job.user_id = user.id
            job.need_blur = False
            job.show_in_profile = True
            job.save()
        else:
            job.pk = None
            job.user_id = user.id
            job.save()

    elif kwargs.get('undress_job_id'):
        from apps.jobs.models import UndressJob
        job: UndressJob = UndressJob.objects.filter(pk=uuid.UUID(kwargs['undress_job_id'])).first()
        if job and job.user_id is None:
            job.user_id = user.id
            job.need_blur = False
            job.show_in_profile = True
            job.save()
