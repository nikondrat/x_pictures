import uuid
from typing import Optional

from django.utils.translation import gettext as _
from rest_framework import mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

import elasticsearch_dsl
from drf_spectacular.utils import OpenApiParameter, extend_schema

from core.common.cached.ram import Cached
from core.users.authentication import UserOrAnonymousAuthentication
from apps.jobs.models import ImageGallery, GenerateJob, VideoGallery
from apps.gallery.rest import paginations
from apps.gallery.rest import serializers
from apps.gallery.rest import utils
from apps.gallery import documents


class ImageGalleryAPIViewSet(GenericViewSet,
                             mixins.RetrieveModelMixin,
                             mixins.ListModelMixin):
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ImageGallerySerializer
    pagination_class = paginations.GalleryPagination
    document_class = documents.GenerateJobDocument

    def get_queryset(self):
        return ImageGallery.objects.select_related(
            'job', 'job__action', 'job__sd_model',
        ).prefetch_related(
            'likes'
        )

    def get_filtered_queryset(self, job_ids: Optional[list] = None,
                              filter_ids: Optional[list] = None,
                              sd_model_id: Optional[int] = None,
                              action_id: Optional[int] = None):
        filters, exclude = {}, {}

        if job_ids:
            filters.update({'job__id__in': job_ids})
        if filter_ids:
            filters.update({'job__filters__id__in': filter_ids})
            exclude.update({'job__filters__id__in': utils.get_exclude_filter_ids(filter_ids=filter_ids)})
        if sd_model_id:
            filters.update({'job__sd_model_id': sd_model_id})
        if action_id:
            filters.update({'job__action_id': action_id})

        return self.get_queryset().filter(
            job__status=GenerateJob.Status.SUCCESS,
        ).exclude(
            job__filters__id=15
        ).exclude(
            **exclude
        ).filter(
            **filters
        ).distinct(
            'job_id'
        )

    @Cached(timeout=60 * 10)
    def search(self, query: str):
        query = elasticsearch_dsl.Q(
            'bool',
            should=[
                elasticsearch_dsl.Q('match', filters__public_name=query),
                elasticsearch_dsl.Q('match', sd_model__public_name=query),
                elasticsearch_dsl.Q('match', action__public_name=query),
            ],
        )
        search = self.document_class.search().query(query)
        return [obj.id for obj in search.execute()]

    @extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: serializers.ImageGalleryFilterSerializer(),
        },
        summary=_('Filter for gallery'),
        description=_('Filter for gallery'),
        exclude=True,
    )
    @action(methods=['GET'], detail=False, url_path='filters', url_name='get_filters')
    def get_filters(self, request: Request, *args, **kwargs):
        filters = utils.get_gallery_filters()
        return Response(
            serializers.ImageGalleryFilterSerializer(
                filters,
            ).data
        )

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='id', type=uuid.UUID, required=True, location=OpenApiParameter.PATH),
        ],
        responses={
            status.HTTP_200_OK: serializers.ImageGalleryDetailSerializer(),
        },
        summary=_('Image in gallery detail'),
        description=_('Image in gallery detail'),
        exclude=True,
    )
    def retrieve(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestImageGalleryDetailSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        likes_structure = utils.get_images_likes_by_qs(
            objs=[serializer.validated_data['obj']],
            user=request.user if request.user.is_authenticated else None,
        )

        return Response(
            serializers.ImageGalleryDetailSerializer(
                serializer.validated_data['obj'],
                context={
                    'user': request.user,
                    'likes_structure': likes_structure,
                },
            ).data
        )

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='query', type=str, required=False),
            OpenApiParameter(name='action_id', type=int, required=False),
            OpenApiParameter(name='sd_model_id', type=int, required=False),
            OpenApiParameter(name='filter_ids', type=str, required=False),
        ],
        summary=_('Image in gallery'),
        description=_('Image in gallery'),
        exclude=True,
    )
    def list(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestImageGallerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        job_ids = []
        if serializer.validated_data.get('query'):
            job_ids = self.search(query=serializer.validated_data['query'])

        qs = self.get_filtered_queryset(
            job_ids=job_ids,
            filter_ids=serializer.validated_data.get('filter_ids'),
            sd_model_id=serializer.validated_data.get('sd_model_id'),
            action_id=serializer.validated_data.get('action_id'),
        )

        page = self.paginate_queryset(qs)

        likes_structure = utils.get_images_likes_by_qs(
            objs=page,
            user=request.user if request.user.is_authenticated else None,
        )

        return self.get_paginated_response(
            self.get_serializer(
                page,
                context={
                    'user': request.user,
                    'likes_structure': likes_structure,
                },
                many=True
            ).data
        )

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='id', type=uuid.UUID, required=True, location=OpenApiParameter.PATH),
        ],
        responses={
            status.HTTP_201_CREATED: serializers.ImageGalleryDetailSerializer(),
        },
        summary=_('Reaction'),
        description=_('Reaction'),
        exclude=True,
    )
    @action(methods=['POST'], detail=True, url_path='reaction', url_name='reaction')
    def reaction(self, request: Request, *args, **kwargs):
        obj = utils.make_reaction(pk=kwargs['pk'], user=request.user)
        return Response(
            status=status.HTTP_201_CREATED,
            data=serializers.ImageGalleryDetailSerializer(obj, context={'user': request.user}).data,
        )


class VideoGalleryAPIViewSet(GenericViewSet,
                             mixins.RetrieveModelMixin,
                             mixins.ListModelMixin):
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ImageGallerySerializer
    pagination_class = paginations.GalleryPagination

    # document_class = documents.GenerateJobDocument

    def get_queryset(self):
        return VideoGallery.objects.filter(
            job__status=GenerateJob.Status.SUCCESS,
        )

    @Cached(timeout=60 * 10)
    def get_filtered_queryset(self, job_ids: Optional[list] = None,
                              filter_ids: Optional[list] = None,
                              sd_model_id: Optional[int] = None,
                              action_id: Optional[int] = None):
        filters = {}
        exclude = {}

        if job_ids:
            filters.update({'job__id__in': job_ids})
        if filter_ids:
            filters.update({'job__filters__id__in': filter_ids})
            exclude.update({'job__filters__id__in': utils.get_exclude_filter_ids(filter_ids=filter_ids)})
        if sd_model_id:
            filters.update({'job__sd_model_id': sd_model_id})

        return self.get_queryset().exclude(job__filters__id=15).exclude(**exclude).filter(**filters).distinct('job_id')

    @Cached(timeout=60 * 10)
    def search(self, query: str):
        query = elasticsearch_dsl.Q(
            'bool',
            should=[
                elasticsearch_dsl.Q('match', filters__public_name=query),
                elasticsearch_dsl.Q('match', sd_model__public_name=query),
                elasticsearch_dsl.Q('match', action__public_name=query),
            ],
        )
        search = self.document_class.search().query(query)
        return [obj.id for obj in search.execute()]

    @extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: serializers.ImageGalleryFilterSerializer(),
        },
        summary=_('Filter for gallery'),
        description=_('Filter for gallery'),
        exclude=True,
    )
    @action(methods=['GET'], detail=False, url_path='filters', url_name='get_filters')
    def get_filters(self, request: Request, *args, **kwargs):
        filters = utils.get_gallery_filters()
        return Response(
            serializers.ImageGalleryFilterSerializer(
                filters,
            ).data
        )

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='id', type=uuid.UUID, required=True, location=OpenApiParameter.PATH),
        ],
        responses={
            status.HTTP_200_OK: serializers.VideoGalleryDetailSerializer(),
        },
        summary=_('Video in gallery detail'),
        description=_('Video in gallery detail'),
        exclude=True,
    )
    def retrieve(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestVideoGalleryDetailSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializers.VideoGalleryDetailSerializer(
                serializer.validated_data['obj'],
                context={
                    'user': request.user,
                },
            ).data
        )

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='query', type=str, required=False),
            OpenApiParameter(name='sd_model_id', type=int, required=False),
            OpenApiParameter(name='filter_ids', type=str, required=False),
        ],
        summary=_('Image in gallery'),
        description=_('Image in gallery'),
        exclude=True,
    )
    def list(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestVideoGallerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        job_ids = []
        if serializer.validated_data.get('query'):
            job_ids = self.search(query=serializer.validated_data['query'])

        qs = self.get_filtered_queryset(
            job_ids=job_ids,
            filter_ids=serializer.validated_data.get('filter_ids'),
            sd_model_id=serializer.validated_data.get('sd_model_id'),
            action_id=serializer.validated_data.get('action_id'),
        )

        page = self.paginate_queryset(qs)

        return self.get_paginated_response(
            self.get_serializer(
                page,
                context={
                    'user': request.user,
                },
                many=True
            ).data
        )

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='id', type=uuid.UUID, required=True, location=OpenApiParameter.PATH),
        ],
        responses={
            status.HTTP_201_CREATED: serializers.ImageGalleryDetailSerializer(),
        },
        summary=_('Reaction'),
        description=_('Reaction'),
        exclude=True,
    )
    @action(methods=['POST'], detail=True, url_path='reaction', url_name='reaction')
    def reaction(self, request: Request, *args, **kwargs):
        obj = utils.make_reaction(pk=kwargs['pk'], user=request.user)
        return Response(
            status=status.HTTP_201_CREATED,
            data=serializers.ImageGalleryDetailSerializer(obj, context={'user': request.user}).data,
        )
