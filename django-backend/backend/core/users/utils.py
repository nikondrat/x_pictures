from typing import Optional

from core.common.cached.ram import Cached
from core.users.models import User


@Cached(timeout=60*60)
def find_user_by_email(email: str) -> bool:
    return User.objects.filter(
        email=email,
    ).exists()


@Cached(timeout=60*60)
def get_user_by_email(email: str) -> Optional[User]:
    return User.objects.filter(
        email=email,
    ).first()


@Cached(timeout=60*60)
def get_user_by_id(user_id: str) -> Optional[User]:
    return User.objects.filter(
        pk=user_id,
    ).first()
