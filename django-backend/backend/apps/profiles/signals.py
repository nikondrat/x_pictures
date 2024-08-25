def remove_file_from_s3(sender, instance, using, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


def _get_profile_type_by_subscription_id(subscription_id: int):
    from apps.profiles.models import ProfileType
    if subscription_id in (1, 2, 6):
        return ProfileType.advance
    elif subscription_id in (3, 4, 12):
        return ProfileType.premium
    else:
        return ProfileType.super_premium


def remove_blur_after_paid_subscription(user_id: str):
    from apps.jobs.models import UndressJob, GenerateJob

    UndressJob.objects.filter(
        user_id=user_id,
        need_blur=True,
    ).update(need_blur=False)

    GenerateJob.objects.filter(
        user_id=user_id,
        need_blur=True,
    ).update(need_blur=False)


def deactivate_subscription_after_create_new(sender, instance, created=False, **kwargs):
    if created:
        from apps.profiles.models import ProfileSubscription

        profile = instance.profile

        ProfileSubscription.objects.exclude(
            id=instance.id,
        ).filter(
            profile=profile,
        ).update(
            is_active=False
        )

        profile.type = _get_profile_type_by_subscription_id(subscription_id=instance.subscription.id)
        profile.balance += instance.subscription.amount
        profile.save()

        remove_blur_after_paid_subscription(user_id=instance.profile.pk)


def deactivate_subscription_after_deleted(sender, instance, using, **kwargs):
    from apps.profiles.models import ProfileType
    profile = instance.profile
    profile.type = ProfileType.basic
    profile.save()
