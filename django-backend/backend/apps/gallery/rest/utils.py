from django.db import transaction
from django.db.models import Q, Count, ExpressionWrapper, BooleanField
from django.db.models.query import Prefetch
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType

from rest_framework.exceptions import NotFound

from core.common.cached.ram import Cached
from core.users.models import User
from apps.jobs import models


@Cached(timeout=60 * 60)
def get_gallery_filters() -> dict:
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
        'collections': get_collections(),
    }


@transaction.atomic()
def make_reaction(pk: int, user: User) -> models.ImageGallery:
    try:
        image_gallery = models.ImageGallery.objects.prefetch_related(
            'likes'
        ).get(job_id=pk)
    except models.ImageGallery.DoesNotExist:
        raise NotFound()

    reaction = image_gallery.likes.filter(author=user).first()
    if not reaction:
        image_gallery.likes.create(author=user)
    else:
        reaction.is_active = not reaction.is_active
        reaction.save()

    return image_gallery


@Cached(timeout=60 * 60)
def _get_exclude_filter_ids(filter_ids: list[int], category_filter_ids: list[int]):
    exclude_filter_ids = []
    count = 0
    for filter_id in category_filter_ids:
        if filter_id not in filter_ids:
            exclude_filter_ids.append(filter_id)
        else:
            count += 1

    if count > 0:
        return exclude_filter_ids
    return []


@Cached(timeout=60 * 10)
def get_exclude_filter_ids(filter_ids: list[int]):
    exclude_filter_ids = []

    for category in models.Category.objects.exclude(pk__in=[1, 2]).filter(is_active=True):
        exclude_filter_ids.extend(_get_exclude_filter_ids(
            filter_ids=filter_ids,
            category_filter_ids=category.filters.filter(is_active=True).values_list('id', flat=True)
        ))

    return exclude_filter_ids


def get_collections():
    # TODO
    return [
        {
            'name': _('Milf'),
            'filter_ids': [],
        },
        {
            'name': _('Teen'),
            'filter_ids': [],
        },
        {
            'name': _('Big Tits'),
            'filter_ids': [],
        },
        {
            'name': _('Anime'),
            'filter_ids': [],
        },
        {
            'name': _('Cartoon'),
            'filter_ids': [],
        }
    ]


def get_images_likes_by_qs(objs, user: User = None):
    qs = models.Like.objects.filter(
        content_type=ContentType.objects.get_for_model(models.ImageGallery).id,
        is_active=True,
        object_id__in=[obj.pk for obj in objs],
    ).values(
        'object_id'
    ).annotate(
        lcount=Count('pk'),
    )
    if user:
        qs = qs.annotate(
            is_reaction=ExpressionWrapper(
                Q(author=user),
                output_field=BooleanField()
            )
        )

    return {
        data['object_id']: {
            'count': data['lcount'],
            'is_reaction': data.get('is_reaction', False),
        }
        for data in qs
    }
