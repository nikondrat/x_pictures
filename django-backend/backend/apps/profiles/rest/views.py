import uuid

from django.utils.translation import gettext as _

from rest_framework import status, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound

from drf_spectacular.utils import OpenApiParameter, extend_schema

from core.users.authentication import ApiTokenAuthentication
from apps.profiles.rest import utils
from apps.profiles.rest import serializers
from apps.profiles.rest import paginations


class ProfileAPIViewSet(GenericViewSet):
    authentication_classes = (ApiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileDetailSerializer
    pagination_class = paginations.StoragePagination

    @extend_schema(
        responses={status.HTTP_200_OK: serializer_class},
        summary=_('Profile info'),
        description=_('Profile info'),
    )
    @action(methods=['GET'], detail=False)
    def me(self, request: Request):
        return Response(self.get_serializer(request.user.profile).data)

    @extend_schema(
        request=serializers.UploadImageSerializer,
        responses={status.HTTP_201_CREATED: serializer_class},
        summary=_('Upload image'),
        description=_('Upload image'),
    )
    @action(methods=['POST'], detail=False, url_path='upload-image', url_name='upload_image')
    def upload_image(self, request: Request):
        serializer = serializers.UploadImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = utils.upload_image(request.user.profile, image_b64=serializer.validated_data['image'])

        return Response(self.get_serializer(profile).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={status.HTTP_201_CREATED: serializer_class},
        summary=_('Delete image'),
        description=_('Delete image'),
    )
    @action(methods=['DELETE'], detail=False, url_path='delete-image', url_name='delete_image')
    def delete_image(self, request: Request):
        profile = utils.delete_image(request.user.profile)
        return Response(self.get_serializer(profile).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
        summary=_('Delete account'),
        description=_('Delete account'),
    )
    @action(methods=['DELETE'], detail=False, url_path='delete-account', url_name='delete_account')
    def delete_account(self, request: Request):
        utils.delete_account(user=request.user)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        request=serializers.UpdateProfileSerializer(),
        responses={status.HTTP_201_CREATED: serializer_class},
        summary=_('Update profile'),
        description=_('Update profile'),
    )
    @action(methods=['PATCH'], detail=False, url_path='update', url_name='update')
    def update_profile(self, request: Request):
        serializer = serializers.UpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.username = serializer.validated_data['username']
        request.user.save()

        return Response(self.get_serializer(request.user.profile).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(
        request=serializers.ChangePasswordSerializer,
        responses={status.HTTP_201_CREATED: serializer_class},
        summary=_('Change password'),
        description=_('Change password'),
    )
    @action(methods=['PATCH'], detail=False, url_path='change-password', url_name='change_password')
    def change_password(self, request: Request):
        serializer = serializers.ChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        request.user = utils.change_password(user=request.user, new_password=serializer.validated_data['new_password'])

        return Response(self.get_serializer(request.user.profile).data,
                        status=status.HTTP_201_CREATED)

    # TODO legacy delete
    @extend_schema(
        request=None,
        responses={status.HTTP_200_OK: serializers.ImageStorageSerializer(many=True)},
        summary=_('Image storage'),
        description=_('Image storage'),
        deprecated=True,
    )
    @action(methods=['GET'], detail=False, url_path='image-storage', url_name='image_storage')
    def image_storage(self, request: Request):
        queryset = utils.get_image_storage_qs(profile=request.user.profile)
        page = self.paginate_queryset(queryset=queryset)
        serializer = serializers.ImageStorageSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class ProfileImageStorageAPIViewSet(GenericViewSet,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin):
    authentication_classes = (ApiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ImageStorageSerializer
    pagination_class = paginations.StoragePagination

    @extend_schema(
        request=None,
        responses={status.HTTP_200_OK: serializers.VideoStorageSerializer(many=True)},
        summary=_('Image storage'),
        description=_('Image storage'),
        exclude=True,
    )
    def list(self, request: Request):
        queryset = utils.get_image_storage_qs(profile=request.user.profile)
        page = self.paginate_queryset(queryset=queryset)
        return self.get_paginated_response(self.get_serializer(
            page,
            many=True,
            context={
                'user': request.user,
            }
        ).data)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='id', required=True, type=uuid.UUID, location=OpenApiParameter.PATH)
        ],
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
        summary=_('Delete an image from storage'),
        description=_('Delete an image from storage'),
        exclude=True,
    )
    def destroy(self, request: Request, *args, **kwargs):
        utils.delete_image_from_storage(user=request.user, pk=kwargs['pk'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileVideoStorageAPIViewSet(GenericViewSet,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin):
    authentication_classes = (ApiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.VideoStorageSerializer
    pagination_class = paginations.StoragePagination

    @extend_schema(
        request=None,
        responses={status.HTTP_200_OK: serializers.VideoStorageSerializer(many=True)},
        summary=_('Video storage'),
        description=_('Video storage'),
        exclude=True,
    )
    def list(self, request: Request):
        queryset = utils.get_video_storage_qs(profile=request.user.profile)
        page = self.paginate_queryset(queryset=queryset)
        return self.get_paginated_response(self.get_serializer(
            page,
            many=True,
            context={
                'user': request.user,
            }
        ).data)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='id', required=True, type=uuid.UUID, location=OpenApiParameter.PATH)
        ],
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
        summary=_('Delete an video from storage'),
        description=_('Delete an video from storage'),
        exclude=True,
    )
    def destroy(self, request: Request, *args, **kwargs):
        utils.delete_video_from_storage(user=request.user, pk=kwargs['pk'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileLikedImageAPIViewSet(GenericViewSet,
                                  mixins.ListModelMixin):
    authentication_classes = (ApiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LikedImageStorageSerializer
    pagination_class = paginations.LikedStoragePagination

    @extend_schema(
        request=None,
        responses={status.HTTP_200_OK: serializers.LikedImageStorageSerializer(many=True)},
        summary=_('Liked image storage'),
        description=_('Image image storage'),
        exclude=True,
    )
    def list(self, request: Request):
        queryset = utils.get_liked_images_qs(profile=request.user.profile)
        page = self.paginate_queryset(queryset=queryset)
        return self.get_paginated_response(self.get_serializer(
            page,
            many=True,
            context={
                'user': request.user,
            }
        ).data)


class ProfileLikedVideoAPIViewSet(GenericViewSet,
                                  mixins.ListModelMixin):
    authentication_classes = (ApiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LikedVideoStorageSerializer
    pagination_class = paginations.LikedStoragePagination

    @extend_schema(
        request=None,
        responses={status.HTTP_200_OK: serializers.LikedVideoStorageSerializer(many=True)},
        summary=_('Liked video storage'),
        description=_('Image video storage'),
        exclude=True,
    )
    def list(self, request: Request):
        queryset = utils.get_liked_video_qs(profile=request.user.profile)
        page = self.paginate_queryset(queryset=queryset)
        return self.get_paginated_response(self.get_serializer(
            page,
            many=True,
            context={
                'user': request.user,
            }
        ).data)


# TODO legacy delete
@extend_schema(
    parameters=[
        OpenApiParameter(name='id', required=True, type=uuid.UUID, location=OpenApiParameter.PATH)
    ],
    request=None,
    responses={status.HTTP_204_NO_CONTENT: None},
    summary=_('Delete an image from storage'),
    description=_('Delete an image from storage'),
    exclude=True,
    deprecated=True,
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([ApiTokenAuthentication])
def delete_image_from_storage_view(request: Request, pk: uuid.UUID):
    utils.delete_image_from_storage(user=request.user, pk=pk)
    return Response(status=status.HTTP_204_NO_CONTENT)


class PatreonAPIViewSet(GenericViewSet,
                        mixins.CreateModelMixin):
    authentication_classes = (ApiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PatreonSerializer

    @extend_schema(
        request=serializers.CreatePatreonSerializer(),
        responses={
            status.HTTP_201_CREATED: serializer_class
        },
        summary=_('Include patreon'),
        description=_('Include patreon'),
    )
    def create(self, request: Request, *args, **kwargs):
        if request.user.profile.has_patreon:
            raise ValidationError({
                'code': _('The patreon account is already connected'),
            })

        serializer = serializers.CreatePatreonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patreon = utils.include_patreon(
            profile=request.user.profile,
            patreon_info=serializer.validated_data['patreon_info'],
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(patreon).data
        )

    @extend_schema(
        request=serializers.CreatePatreonSerializer(),
        responses={
            status.HTTP_201_CREATED: serializer_class
        },
        summary=_('Get patreon'),
        description=_('Get patreon'),
    )
    @action(methods=['GET'], detail=False, url_path='info', url_name='info')
    def get_patreon_info(self, request: Request,):
        if not request.user.profile.has_patreon:
            raise NotFound()

        return Response(serializers.PatreonSerializer(
            request.user.profile.patreon,
        ).data)
