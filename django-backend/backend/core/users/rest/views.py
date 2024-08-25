import uuid

from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from rest_framework import status, exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from drf_spectacular.utils import OpenApiParameter, extend_schema

import settings
from core.common.alanbase import client as alanbase_client

from core.users import models
from core.users.services import resend_email
from core.users.authentication import ApiTokenAuthentication
from core.users.rest import utils
from core.users.rest import serializers


class RegisterAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @classmethod
    def post_registration(cls, user: models.User):
        if user.click_id:
            alanbase_client.make_registration(
                click_id=user.click_id,
                user_id=user.pk,
            )
        else:
            alanbase_client.make_registration_without_click_id(
                user_id=user.pk,
            )

    @classmethod
    def add_job_after_registration(cls, user: models.User,
                                   generate_job_id: str = None,
                                   undress_job_id: str = None):
        try:
            utils.add_job_after_registration(
                user=user,
                generate_job_id=generate_job_id,
                undress_job_id=undress_job_id
            )
        except Exception:
            pass

    @extend_schema(
        parameters=[
            OpenApiParameter(name='click_id', required=False, description=_('Alan Base click id'), type=str),
            OpenApiParameter(name='generate_job_id', required=False, description=_('Generate id'), type=uuid.UUID),
            OpenApiParameter(name='undress_job_id', required=False, description=_('Generate id'), type=uuid.UUID),
        ],
        request=serializers.RegisterSerializer,
        responses={status.HTTP_200_OK: serializers.TokenSerializer},
        summary=_('Register'),
        description=_('Register'),
    )
    def post(self, request: Request):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, token = utils.registration_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            auth_provider=models.User.AuthProvider.email,
            click_id=request.query_params.get('click_id'),
            ip_address=serializer.validated_data.get('ip_address'),
        )

        self.post_registration(user=user)
        self.add_job_after_registration(user=user,
                                        generate_job_id=request.query_params.get('generate_job_id'),
                                        undress_job_id=request.query_params.get('undress_job_id'))

        return Response(serializers.TokenSerializer(token).data)


class LoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @extend_schema(
        request=serializers.LoginSerializer,
        responses={status.HTTP_200_OK: serializers.TokenSerializer},
        summary=_('Login'),
        description=_('Login'),
    )
    def post(self, request: Request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = utils.login_user(user=serializer.validated_data['user'])
        return Response(serializers.TokenSerializer(token).data)


@extend_schema(
    parameters=[
        OpenApiParameter(name='token', description='Token', required=True, type=str),
    ],
    responses={status.HTTP_302_FOUND: None},
    summary=_('Verification by token'),
    description=_('Verification by token'),
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def verification_view(request: Request, token: str = None):
    if token:
        utils.verification_user(token=token)
    return HttpResponseRedirect(settings.FRONT_DOMAIN)


@extend_schema(
    request=None,
    responses={status.HTTP_204_NO_CONTENT: None},
    summary=_('Refresh verification message'),
    description=_('Refresh verification message'),
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([ApiTokenAuthentication])
def refresh_verification_view(request: Request):
    if request.user.is_verified:
        raise exceptions.ValidationError({
            '__all__': _('Already verified')
        })

    resend_email(
        user_id=request.user.pk,
        typ=models.EmailMessage.MessageType.verification,
        email=request.user.email,
    )

    return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetAPIViewSet(GenericViewSet):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @extend_schema(
        request=serializers.PasswordResetSerializer(),
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    @action(methods=['POST'], detail=False, url_path='send', url_name='send')
    def send_message(self, request: Request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resend_email(
            user_id=serializer.validated_data['user'].pk,
            typ=models.EmailMessage.MessageType.password_reset,
            email=serializer.validated_data['email'],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=serializers.SetNewPasswordSerializer(),
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    @action(methods=['POST'], detail=False, url_path='set', url_name='set')
    def set_new_password(self, request: Request):
        serializer = serializers.SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        utils.password_reset(user=serializer.validated_data['user'],
                             new_password=serializer.validated_data['new_password'],
                             token=serializer.validated_data['token'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class SocialMediaAuthAPIViewSet(GenericViewSet):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @classmethod
    def post_registration(cls, user: models.User):
        if user.click_id:
            alanbase_client.make_registration(
                click_id=user.click_id,
                user_id=user.pk,
            )
        else:
            alanbase_client.make_registration_without_click_id(
                user_id=user.pk,
            )

    @classmethod
    def add_job_after_registration(cls, user: models.User,
                                   generate_job_id: str = None,
                                   undress_job_id: str = None):
        try:
            utils.add_job_after_registration(
                user=user,
                generate_job_id=generate_job_id,
                undress_job_id=undress_job_id
            )
        except Exception:
            pass

    @extend_schema(
        parameters=[
            OpenApiParameter(name='click_id', required=False, description=_('Alan Base click id'), type=str),
            OpenApiParameter(name='generate_job_id', required=False, description=_('Generate id'), type=uuid.UUID),
            OpenApiParameter(name='undress_job_id', required=False, description=_('Generate id'), type=uuid.UUID),
        ],
        request=serializers.GoogleAuthSerializer(),
        responses={status.HTTP_200_OK: serializers.TokenSerializer}
    )
    @action(methods=['POST'], detail=False, url_path='google-auth', url_name='google_auth')
    def google_auth(self, request: Request):
        serializer = serializers.GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, token, registered = utils.social_media_auth(
            email=serializer.validated_data['email'],
            auth_provider=models.User.AuthProvider.google,
            click_id=request.query_params.get('click_id'),
            ip_address=serializer.validated_data.get('ip_address'),
        )

        if registered:
            self.post_registration(user=user)
            self.add_job_after_registration(user=user,
                                            generate_job_id=request.query_params.get('generate_job_id'),
                                            undress_job_id=request.query_params.get('undress_job_id'))

        return Response(serializers.TokenSerializer(token).data)


class MarketingAPIViewSet(GenericViewSet):
    authentication_classes = (ApiTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=serializers.AlanBaseSerializer(),
        responses={status.HTTP_204_NO_CONTENT: None},
        summary=_('AlanBase'),
        description=_('AlanBase'),
    )
    @action(methods=['PATCH'], detail=False, url_path='alanbase', url_name='alanbase')
    def alanbase(self, request: Request):
        serializer = serializers.AlanBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        alanbase, _ = models.AlanBase.objects.get_or_create(user=request.user)
        alanbase.sub_id5 = serializer.validated_data['sub_id5']
        alanbase.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
