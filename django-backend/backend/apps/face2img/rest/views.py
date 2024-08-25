import uuid

from django.utils.translation import gettext as _

from rest_framework import mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer

from core.users.authentication import UserOrAnonymousAuthentication
from apps.face2img.rest import paginations
from apps.face2img import models
from apps.face2img.rest import serializers
from apps.jobs import config
from apps.face2img.rest import services


class LoraAPIViewSet(GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin):
    job_cost = config.COST_LORA_TRAINING

    serializer_class = serializers.LoraSerializer
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = paginations.LoraPagination

    def get_queryset(self):
        return models.Lora.objects.filter(
            user=self.request.user,
        ).prefetch_related('training_faces')

    @extend_schema(
        responses={status.HTTP_200_OK: serializers.LoraSerializer(many=True)},
        summary=_("Get my loras"),
        description=_("Get my loras"),
    )
    def list(self, request: Request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied(_('You do not have permission to view this page'))

        qs = self.get_queryset().exclude(
            status__in=[models.Lora.Status.ERROR, models.Lora.Status.CREATED],
        )
        page = self.paginate_queryset(qs)

        return self.get_paginated_response(self.get_serializer(page, many=True).data)

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='id', type=uuid.UUID, required=True, location=OpenApiParameter.PATH),
        ],
        responses={status.HTTP_200_OK: serializers.LoraSerializer()},
        summary=_("Get lora"),
        description=_("Get lora"),
    )
    def retrieve(self, request: Request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied(_('You do not have permission to view this page'))

        serializer = serializers.RequestLoraSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        lora = self.get_queryset().filter(id=serializer.validated_data['id']).first()
        if not lora:
            raise NotFound(_('Lora not found'))

        return Response(self.get_serializer(lora).data)

    @extend_schema(
        request={"multipart/form-data": inline_serializer(
            name="InlineFormSerializer",
            fields={
                "file1": serializers.serializers.ImageField(),
                "file2": serializers.serializers.ImageField(),
                "file3": serializers.serializers.ImageField(),
                "file4": serializers.serializers.ImageField(),
                "file5": serializers.serializers.ImageField(),
                "file6": serializers.serializers.ImageField(),
                "file7": serializers.serializers.ImageField(),
                "file8": serializers.serializers.ImageField(),
                "file9": serializers.serializers.ImageField(),
            },
        )},
        responses={status.HTTP_200_OK: serializers.LoraSerializer()},
        summary=_("Generate new lora"),
        description=_("Generate new lora"),
    )
    def create(self, request: Request, *args, **kwargs):
        lora = services.create_lora(
            user=request.user,
            cost=self.job_cost,
            files=[
                request.data['file1'],
                request.data['file2'],
                request.data['file3'],
                request.data['file4'],
                request.data['file5'],
                request.data['file6'],
                request.data['file7'],
                request.data['file8'],
                request.data['file9'],
            ]
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data=serializers.LoraSerializer(lora).data,
        )


class PackAPIViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = serializers.PackSerializer
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = paginations.PackPagination

    def get_queryset(self):
        return models.Pack.objects.filter(
            is_active=True,
        ).prefetch_related('images')

    @extend_schema(
        responses={status.HTTP_200_OK: serializers.PackSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name='category', type=str, required=False, enum=models.Pack.Category, location=OpenApiParameter.QUERY
            ),
        ],
        summary=_("Get packs"),
        description=_("Get packs"),
    )
    def list(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestPackSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        qs = self.get_queryset()
        if serializer.validated_data.get('category'):
            qs = qs.filter(category=serializer.validated_data['category'])

        page = self.paginate_queryset(qs)
        return self.get_paginated_response(self.get_serializer(page, many=True).data)


class Face2ImgJobAPIViewSet(GenericViewSet,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.ListModelMixin):
    job_cost = config.COST_FACE2IMG_JOB

    serializer_class = serializers.Face2ImgJobSerializer
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = paginations.Face2ImgPagination

    def get_queryset(self):
        return (
            models.Face2ImgJob.objects
            .select_related('lora', 'pack')
            .prefetch_related('results')
            .filter(
                lora__user=self.request.user,
            )
        )

    @extend_schema(
        responses={status.HTTP_200_OK: serializers.Face2ImgJobSerializer(many=True)},
        summary=_("Get my face2img jobs"),
        description=_("Get my face2img jobs"),
    )
    def list(self, request: Request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied(_('You do not have permission to view this page'))

        queryset = (
            self.get_queryset()
            .exclude(status=models.Face2ImgJob.Status.ERROR)
        )
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        responses={status.HTTP_200_OK: serializers.Face2ImgJobSerializer()},
        summary=_("Get face2img job"),
        description=_("Get face2img job"),
    )
    def retrieve(self, request: Request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied(_('You do not have permission to view this page'))

        serializer = serializers.RequestFace2ImgJobSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        job = (
            self.get_queryset()
            .filter(id=serializer.validated_data['id'])
            .first()
        )
        if not job:
            raise NotFound(_('Job not found'))

        return Response(self.get_serializer(job).data)

    @extend_schema(
        responses={status.HTTP_201_CREATED: serializers.Face2ImgJobSerializer()},
        summary=_("Create face2img job"),
        description=_("Create face2img job"),
    )
    def create(self, request: Request, *args, **kwargs):
        serializer = serializers.CreateFace2ImgJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lora = models.Lora.objects.filter(id=serializer.validated_data['lora_id']).first()
        if not lora:
            raise NotFound(_('Lora not found'))

        pack = models.Pack.objects.filter(id=serializer.validated_data['pack_id']).first()
        if not pack:
            raise NotFound(_('Pack not found'))

        job = services.create_face2img_job(
            user=request.user,
            lora=lora,
            pack=pack,
            cost=self.job_cost,
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(job).data,
        )
