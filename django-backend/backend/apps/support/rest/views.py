from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema

from apps.support.rest import serializers
from apps.support.models import SupportMessage


class SupportMessageView(GenericAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @extend_schema(
        request=serializers.SupportMessageSerializer,
        responses={204: None},
        summary=_('Support message'),
        description=_('Support message'),
    )
    def post(self, request: Request):
        serializer = serializers.SupportMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = '999:00000'
        SupportMessage.objects.create(
            user_id=user_id,
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
            message=serializer.validated_data['message'],
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
