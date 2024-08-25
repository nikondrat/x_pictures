import uuid

from django.utils.translation import gettext as _

from rest_framework import mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from drf_spectacular.utils import extend_schema, OpenApiParameter

from core.users.authentication import UserOrAnonymousAuthentication
from apps.jobs import models
from apps.jobs.rest import utils
from apps.jobs.rest import serializers
from apps.jobs.core import (
    UndressService, UndressWithoutMaskService,
    GenerateService, InstagramUndressService,
    VideoService, WhiteGenerateService,
)

from apps.jobs import config


class UndressAPIViewSet(GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin):
    job_cost = config.COST_UNDRESS
    job_without_mask_cost = config.COST_UNDRESS_WITHOUT_MASK

    serializer_class = serializers.UndressJobSerializer
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return models.UndressJob.objects.filter()

    @extend_schema(
        responses={status.HTTP_200_OK: serializers.UndressFilterSerializer()},
        summary=_('Get filters for Undress'),
        description=_('Get filters for Undress'),
        exclude=True,
    )
    @action(methods=['GET'], detail=False, url_path='filters', url_name='get_filters')
    def get_filters(self, request: Request, *args, **kwargs):
        filters = utils.get_undress_filters(
            cost=self.job_cost,
            cost_without_mask=self.job_without_mask_cost,
        )
        return Response(serializers.UndressFilterSerializer(filters).data)

    @extend_schema(
        request=serializers.CreateUndressJobSerializer(),
        responses={status.HTTP_201_CREATED: serializer_class},
        summary=_('Create a undress task'),
        description=_('Create a undress task'),
        exclude=True,
    )
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateUndressJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = UndressService.make_job(
            user=self.request.user,
            filter_ids=serializer.validated_data['filter_ids'],
            image_b64=serializer.validated_data['image_b64'],
            mask_b64=serializer.validated_data['mask_b64'],
            cost=self.job_cost,
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(
                job,
                context={'user': request.user}
            ).data
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name='id', required=True, location=OpenApiParameter.PATH, type=uuid.UUID),
        ],
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_201_CREATED: serializer_class,
        },
        summary=_('Get job information'),
        description=_('Get job information'),
        exclude=True,
    )
    def retrieve(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestJobSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        job = self.get_queryset().filter(pk=serializer.validated_data['pk']).first()
        if not job:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': _('Job not found')}
            )

        status_code = status.HTTP_200_OK
        if job.status in (models.UndressJob.Status.CREATED,
                          models.UndressJob.Status.PROCESS):
            status_code = status.HTTP_201_CREATED

        return Response(
            status=status_code,
            data=self.get_serializer(
                job,
                context={'user': request.user}
            ).data
        )

    @extend_schema(
        responses={
            status.HTTP_200_OK: serializers.UndressJobSerializer(many=True),
        },
        summary=_('Last generate'),
        description=_('Last generate'),
        exclude=True,
    )
    def list(self, request: Request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()

        qs = self.get_queryset().filter(
            user_id=request.user.id,
            status=models.UndressJob.Status.SUCCESS,
            show_in_profile=True,
        ).order_by('-created')

        return Response(
            self.get_serializer(
                qs[:10],
                context={'user': request.user},
                many=True,
            ).data,
        )

    @extend_schema(
        request=None,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        summary=_('Clean history'),
        description=_('Clean history'),
        exclude=True,
    )
    @action(methods=['DELETE'], detail=False, url_path='clean-history', url_name='clean_history')
    def clean_history(self, request: Request, *args, **kwargs):
        if not request.user.profile.is_premium:
            raise PermissionDenied(_('You do not have permission to clean history'))

        models.UndressJob.objects.filter(
            user_id=request.user.pk,
            status=models.UndressJob.Status.SUCCESS,
            show_in_profile=True
        ).update(
            show_in_profile=False,
        )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class UndressWithoutMaskAPIViewSet(GenericViewSet,
                                   mixins.CreateModelMixin):
    job_cost = config.COST_UNDRESS_WITHOUT_MASK

    serializer_class = serializers.UndressJobSerializer
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return models.UndressJob.objects.filter()

    @extend_schema(
        request=serializers.CreateUndressJobWithoutMaskSerializer(),
        responses={
            status.HTTP_201_CREATED: serializers.UndressJobSerializer(),
        },
        summary=_('Create a undress without mask task'),
        description=_('Create a undress without mask task'),
        exclude=True,
    )
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateUndressJobWithoutMaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = UndressWithoutMaskService.make_job(
            user=self.request.user,
            filter_ids=serializer.validated_data['filter_ids'],
            image_b64=serializer.validated_data['image_b64'],
            cost=self.job_cost,
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(
                job,
                context={'user': request.user}
            ).data
        )


class GenerateAPIViewSet(GenericViewSet,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin):
    job_cost = config.COST_GENERATE

    serializer_class = serializers.GenerateJobSerializer
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return models.GenerateJob.objects.filter()

    @extend_schema(
        parameters=[
            OpenApiParameter(name='sd_model_id', required=False),
        ],
        responses={status.HTTP_200_OK: serializers.GenerateFilterSerializer()},
        summary=_('Get filters for Generate'),
        description=_('Get filters for Generate'),
        exclude=True,
    )
    @action(methods=['GET'], detail=False, url_path='filters', url_name='get_filters')
    def get_filters(self, request: Request, *args, **kwargs):
        filters = utils.get_generate_filters(
            cost=self.job_cost,
            sd_model_id=request.query_params.get('sd_model_id'),
        )
        return Response(serializers.GenerateFilterSerializer(filters, context={'user': request.user}).data)

    @extend_schema(
        request=serializers.CreateGenerateJobSerializer(),
        responses={status.HTTP_201_CREATED: serializer_class},
        summary=_('Create a generate task'),
        description=_('Create a generate task'),
        exclude=True,
    )
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateGenerateJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = GenerateService.make_job(
            user=self.request.user,
            filter_ids=serializer.validated_data['filter_ids'],
            sd_model_id=serializer.validated_data['sd_model_id'],
            action_id=serializer.validated_data['action_id'],
            cost=self.job_cost,
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(
                job,
                context={'user': request.user}
            ).data
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name='id', required=True, location=OpenApiParameter.PATH, type=uuid.UUID),
        ],
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_201_CREATED: serializer_class,
        },
        summary=_('Get job information'),
        description=_('Get job information'),
        exclude=True,
    )
    def retrieve(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestJobSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        job = self.get_queryset().filter(pk=serializer.validated_data['pk']).first()
        if not job:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': _('Job not found')}
            )

        status_code = status.HTTP_200_OK
        if job.status in (models.UndressJob.Status.CREATED,
                          models.UndressJob.Status.PROCESS):
            status_code = status.HTTP_201_CREATED

        return Response(
            status=status_code,
            data=self.get_serializer(
                job,
                context={'user': request.user}
            ).data
        )

    @extend_schema(
        responses={
            status.HTTP_200_OK: serializers.GenerateJobSerializer(many=True),
        },
        summary=_('Last generate'),
        description=_('Last generate'),
        exclude=True,
    )
    def list(self, request: Request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()

        qs = self.get_queryset().filter(
            user_id=request.user.id,
            status=models.GenerateJob.Status.SUCCESS,
            show_in_profile=True,
        ).order_by('-created')

        return Response(
            self.get_serializer(
                qs[:10],
                context={'user': request.user},
                many=True
            ).data,
        )


class InstagramUndressAPIViewSet(GenericViewSet,
                                 mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin):
    parser_cost = config.COST_INSTAGRAM_PARSER
    job_cost = config.COST_INSTAGRAM_UNDRESS

    serializer_class = serializers.InstagramUndressJobSerializer
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return models.InstagramUndressJob.objects.filter()

    @extend_schema(
        responses={status.HTTP_200_OK: serializers.InstagramUndressFilterSerializer()},
        summary=_('Get filters for Instagram undress'),
        description=_('Get filters for Instagram undress'),
        exclude=True,
    )
    @action(methods=['GET'], detail=False, url_path='filters', url_name='filters')
    def filters(self, request: Request):
        filters = utils.get_instagram_undress_filters(parsing_cost=self.parser_cost,
                                                      undress_cost_per_image=self.job_cost)
        return Response(serializers.InstagramUndressFilterSerializer(filters).data)

    @extend_schema(
        request=serializers.InstagramUndressParsingSerializer(),
        responses={status.HTTP_201_CREATED: serializers.InstagramUndressJobSerializer()},
        summary=_('Start parsing instagram'),
        description=_('Start parsing instagram'),
        exclude=True,
    )
    @action(methods=['POST'], detail=False, url_path='start-parsing', url_name='start_parsing')
    def start_parsing(self, request: Request):
        serializer = serializers.InstagramUndressParsingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = InstagramUndressService.create_step1(
            user=request.user,
            cost=self.parser_cost,
            link=serializer.validated_data['link'],
            qty=serializer.validated_data['qty'],
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(job, context={'user': request.user}).data,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name='id', required=True, location=OpenApiParameter.PATH, type=uuid.UUID),
        ],
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_201_CREATED: serializer_class,
        },
        summary=_('Get job information'),
        description=_('Get job information'),
        exclude=True,
    )
    def retrieve(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestJobSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        job = self.get_queryset().filter(
            pk=serializer.validated_data['pk']
        ).prefetch_related(
            'sources', 'jobs',
        ).first()
        if not job:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': _('Job not found')}
            )

        status_code = status.HTTP_200_OK
        if job.status in (models.UndressJob.Status.CREATED,
                          models.UndressJob.Status.PROCESS):
            status_code = status.HTTP_201_CREATED

        return Response(
            status=status_code,
            data=self.get_serializer(job, context={
                'user': request.user,
            }).data
        )

    @extend_schema(
        request=serializers.CreateInstagramUndressJobSerializer(),
        responses={status.HTTP_201_CREATED: serializer_class},
        summary=_('Create a instagram undress task'),
        description=_('Create a instagram undress task'),
        exclude=True,
    )
    def create(self, request: Request, *args, **kwargs):
        serializer = serializers.CreateInstagramUndressJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = InstagramUndressService.create_step2(
            user=request.user,
            cost=self.job_cost,
            job=serializer.validated_data['job'],
            filter_ids=serializer.validated_data['filter_ids'],
            exclude_ids=serializer.validated_data['exclude_ids'],
            custom_masks=serializer.validated_data['custom_masks'],
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(job, context={'user': request.user}).data,
        )


class VideoAPIViewSet(GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin):
    job_cost = config.COST_VIDEO

    serializer_class = serializers.VideoJobSerializer
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return models.VideoJob.objects.filter()

    @extend_schema(
        parameters=[
            OpenApiParameter(name='sd_model_id', required=False),
        ],
        responses={status.HTTP_200_OK: serializers.VideoJobFilterSerializer()},
        summary=_('Get filters for video job'),
        description=_('Get filters for video job'),
        exclude=True,
    )
    @action(methods=['GET'], detail=False, url_path='filters', url_name='filters')
    def filters(self, request: Request):
        filters = utils.get_video_filters(
            cost=self.job_cost,
            sd_model_id=request.query_params.get('sd_model_id'),
        )
        return Response(serializers.VideoJobFilterSerializer(filters, context={'user': request.user}).data)

    @extend_schema(
        request=serializers.CreateVideoJobSerializer(),
        responses={status.HTTP_201_CREATED: serializer_class},
        summary=_('Create a video task'),
        description=_('Create a video task'),
        exclude=True,
    )
    def create(self, request: Request, *args, **kwargs):
        serializer = serializers.CreateVideoJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = VideoService.make_job(
            user=self.request.user,
            filter_ids=serializer.validated_data['filter_ids'],
            sd_model_id=serializer.validated_data['sd_model_id'],
            cost=self.job_cost,
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(
                job,
                context={'user': request.user},
            ).data,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name='id', required=True, location=OpenApiParameter.PATH, type=uuid.UUID),
        ],
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_201_CREATED: serializer_class,
        },
        summary=_('Get job information'),
        description=_('Get job information'),
        exclude=True,
    )
    def retrieve(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestJobSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        job = self.get_queryset().filter(pk=serializer.validated_data['pk']).first()
        if not job:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': _('Job not found')}
            )

        status_code = status.HTTP_200_OK
        if job.status in (models.UndressJob.Status.CREATED,
                          models.UndressJob.Status.PROCESS):
            status_code = status.HTTP_201_CREATED

        return Response(
            status=status_code,
            data=self.get_serializer(
                job,
                data=self.get_serializer(
                    job,
                    context={'user': request.user},
                ).data,
            ).data
        )

    @extend_schema(
        responses={
            status.HTTP_200_OK: serializers.GenerateJobSerializer(many=True),
        },
        summary=_('Last generate'),
        description=_('Last generate'),
        exclude=True,
    )
    def list(self, request: Request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()

        qs = self.get_queryset().filter(
            user_id=request.user.id,
            status=models.VideoJob.Status.SUCCESS,
            show_in_profile=True,
        ).order_by('-created')

        return Response(
            self.get_serializer(
                qs[:10],
                context={'user': request.user},
                many=True,
            ).data,
        )

    @extend_schema(
        request=None,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        summary=_('Clean history'),
        description=_('Clean history'),
        exclude=True,
    )
    @action(methods=['DELETE'], detail=False, url_path='clean-history', url_name='clean_history')
    def clean_history(self, request: Request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied(_('You do not have permission to clean history'))

        models.VideoJob.objects.filter(
            user_id=request.user.pk,
            status=models.VideoJob.Status.SUCCESS,
            show_in_profile=True
        ).update(
            show_in_profile=False,
        )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class WhiteGenerateAPIViewSet(GenericViewSet,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin):
    job_cost = config.COST_GENERATE

    serializer_class = serializers.GenerateJobSerializer
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return models.GenerateJob.objects.filter()

    @extend_schema(
        responses={status.HTTP_200_OK: serializers.GenerateFilterSerializer()},
        summary=_('Get filters for Generate'),
        description=_('Get filters for Generate'),
    )
    @action(methods=['GET'], detail=False, url_path='filters', url_name='get_filters')
    def get_filters(self, request: Request, *args, **kwargs):
        filters = utils.get_white_generate_filters(
            cost=self.job_cost,
        )
        return Response(serializers.GenerateFilterSerializer(filters, context={'user': request.user}).data)

    @extend_schema(
        request=serializers.CreateWhiteGenerateJobSerializer(),
        responses={status.HTTP_201_CREATED: serializer_class},
        summary=_('Create a generate task'),
        description=_('Create a generate task'),
    )
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateWhiteGenerateJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = WhiteGenerateService.make_job(
            user=self.request.user,
            prompt=serializer.validated_data['prompt'],
            sd_model_id=serializer.validated_data['sd_model_id'],
            negative_prompt=serializer.validated_data['negative_prompt'],
            cost=self.job_cost,
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(
                job,
                context={'user': request.user}
            ).data
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name='id', required=True, location=OpenApiParameter.PATH, type=uuid.UUID),
        ],
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_201_CREATED: serializer_class,
        },
        summary=_('Get job information'),
        description=_('Get job information'),
    )
    def retrieve(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestJobSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        job = self.get_queryset().filter(pk=serializer.validated_data['pk']).first()
        if not job:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': _('Job not found')}
            )

        status_code = status.HTTP_200_OK
        if job.status in (models.UndressJob.Status.CREATED,
                          models.UndressJob.Status.PROCESS):
            status_code = status.HTTP_201_CREATED

        return Response(
            status=status_code,
            data=self.get_serializer(
                job,
                context={'user': request.user}
            ).data
        )

    @extend_schema(
        responses={
            status.HTTP_200_OK: serializers.GenerateJobSerializer(many=True),
        },
        summary=_('Last generate'),
        description=_('Last generate'),
    )
    def list(self, request: Request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()

        qs = self.get_queryset().filter(
            user_id=request.user.id,
            status=models.GenerateJob.Status.SUCCESS,
            show_in_profile=True,
            sd_model_id=12,
        ).order_by('-created')

        return Response(
            self.get_serializer(
                qs[:10],
                context={'user': request.user},
                many=True
            ).data,
        )
