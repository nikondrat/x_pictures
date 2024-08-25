from apps.profiles.models import Profile, ProfileSubscription


def has_active_subscription(profile: Profile, *, return_obj: bool = False):
    profile_subscriptions = ProfileSubscription.objects.filter(
        profile=profile,
        is_active=True,
    )
    for profile_subscription in profile_subscriptions:
        if not profile_subscription.is_expired:
            if return_obj:
                return profile_subscription
            return True
    else:
        if return_obj:
            return None
        return False
