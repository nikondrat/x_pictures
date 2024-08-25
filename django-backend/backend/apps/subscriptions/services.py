"""
ВАЖНО:
Если меняется количество генераций или раздеваний
То нужно изменить и в api.undress и api.generate
"""

from datetime import timedelta


class BaseSubscriptionService:
    pk: int
    life_time: timedelta = timedelta(days=30)

    generation_limit_per_period: int
    undress_limit_per_period: int
    photo_storage_limit: int

    save_photo_limit: int = 0

    name: str


class FreeSubscriptionService(BaseSubscriptionService):
    pk = 1
    life_time: timedelta = timedelta(days=30)
    generation_limit_per_period = 3
    undress_limit_per_period = 0
    photo_storage_limit = 5

    name = 'free'


class BasicSubscriptionService(BaseSubscriptionService):
    pk = 2
    generation_limit_per_period = 31_000
    undress_limit_per_period = 40
    photo_storage_limit = 15
    save_photo_limit = 10

    name = 'silver'


class PremiumSubscriptionService(BaseSubscriptionService):
    pk = 3
    generation_limit_per_period = 31_000
    undress_limit_per_period = 90
    photo_storage_limit = 30
    save_photo_limit = 100

    name = 'gold'


class UltraPremiumSubscriptionService(PremiumSubscriptionService):
    """Premium subscription for 1 year"""
    pk = 4
    life_time: timedelta = timedelta(days=30 * 12)
    generation_limit_per_period = PremiumSubscriptionService.generation_limit_per_period * 12
    undress_limit_per_period = PremiumSubscriptionService.undress_limit_per_period * 12
    photo_storage_limit = PremiumSubscriptionService.photo_storage_limit * 12
    save_photo_limit = PremiumSubscriptionService.save_photo_limit * 12
