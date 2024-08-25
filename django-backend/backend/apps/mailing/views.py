from django.http.response import HttpResponseRedirect

from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes

from drf_spectacular.utils import OpenApiParameter, extend_schema

from apps.mailing.services import FirstEvent2024


@extend_schema(
    parameters=[
        OpenApiParameter(name='secret_code', required=True, location=OpenApiParameter.PATH, type=str),
    ],
    request=None,
    responses={status.HTTP_302_FOUND: None},
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def first_event_2024_view(request: Request, secret_code: str):
    redirect_url = FirstEvent2024.handler(secret_code=secret_code)
    return HttpResponseRedirect(redirect_url)
