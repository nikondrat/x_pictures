import decimal
from typing import Optional

from django.db.models.query import Prefetch

from core.common.cached.ram import Cached
from apps.jobs import models


@Cached(timeout=60*60)
def get_sd_model_available_in(sd_model: models.SDModel) -> Optional[int]:
    if sd_model.pk in (2, 8, 7):
        return None
    elif sd_model.pk in (6, 3):
        return 6        # Advance (year)
    elif sd_model.pk in (4, 5):
        return 5        # Premium (year)


@Cached(timeout=60*60, use_inner_cache=True)
def get_undress_filters(cost, cost_without_mask) -> dict:
    categories = models.Category.objects.filter(
        is_active=True,
        type=models.Type.undress,
    ).prefetch_related(Prefetch(
        'filters',
        queryset=models.Filter.objects.filter(is_active=True).order_by('id')
    )).order_by('id')
    return {
        'categories': categories,
        'cost': cost,
        'cost_without_mask': cost_without_mask,
    }


@Cached(timeout=60*60, use_inner_cache=True)
def get_generate_filters(cost: float | int | decimal.Decimal, sd_model_id: Optional[int] = None) -> dict:
    current_sd_model_id = sd_model_id or 2  # Default

    sd_models = models.SDModel.objects.filter(
        type=models.Type.generate,
        is_active=True,
    )
    tags = models.Tag.objects.filter(
        is_active=True,
        categories__type=models.Type.generate,
    ).prefetch_related(Prefetch(
        'categories',
        queryset=models.Category.objects.filter(
            is_active=True,
        ).prefetch_related(Prefetch(
            'filters',
            queryset=models.Filter.objects.filter(
                is_active=True,
            )
        ))
    )).distinct('id')
    return {
        'tags': tags,
        'current_sd_model_id': current_sd_model_id,
        'sd_models': sd_models,
        'actions': models.Action.objects.filter(sd_model_id=current_sd_model_id),
        'cost': cost,
    }


@Cached(timeout=60*60, use_inner_cache=True)
def get_instagram_undress_filters(parsing_cost, undress_cost_per_image) -> dict:
    categories = models.Category.objects.filter(
        is_active=True,
        type=models.Type.undress,
    ).prefetch_related(Prefetch(
        'filters',
        queryset=models.Filter.objects.filter(is_active=True).order_by('id')
    )).order_by('id')
    return {
        'categories': categories,
        'parsing_cost': parsing_cost,
        'undress_cost_per_image': undress_cost_per_image,
    }


@Cached(timeout=60*60, use_inner_cache=True)
def get_video_filters(cost: float | int | decimal.Decimal, sd_model_id: Optional[int] = None) -> dict:
    current_sd_model_id = sd_model_id or 9

    sd_models = models.SDModel.objects.filter(
        type=models.Type.video,
        is_active=True,
    ).exclude(
        id__in=(12,)
    )

    tags = models.Tag.objects.filter(
        is_active=True,
        categories__type=models.Type.generate,      # TODO video type
    ).prefetch_related(Prefetch(
        'categories',
        queryset=models.Category.objects.filter(
            is_active=True,
        ).prefetch_related(Prefetch(
            'filters',
            queryset=models.Filter.objects.filter(
                is_active=True,
            )
        ))
    )).distinct('id')

    return {
        'tags': tags,
        'current_sd_model_id': current_sd_model_id,
        'sd_models': sd_models,
        'cost': cost,
    }


@Cached(timeout=60*60, use_inner_cache=True)
def get_white_generate_filters(cost: float | int | decimal.Decimal) -> dict:

    sd_models = models.SDModel.objects.filter(
        type=models.Type.generate,
        is_active=True,
        id__in=(12,)
    )

    return {
        'tags': [],
        'current_sd_model_id': 12,
        'sd_models': sd_models,
        'actions': models.Action.objects.filter(sd_model_id=12),
        'cost': cost,
    }
