import json

from django.db import transaction

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiRequest

from apps.shop.models import GatewayType, PaymentOrder
from apps.shop.gate import get_payment_gateway
from apps.shop.rest.permissions import (
    IvendPayApiKeyPermission,
    PayAdmitSignaturePermission,
    ArkPayWebhookSignaturePermission
)


@extend_schema(
    parameters=[
        OpenApiParameter(name='HTTP_X_API_KEY', description='Ivendpay secret key', required=True,
                         location=OpenApiParameter.HEADER, type=str)
    ],
    responses={status.HTTP_204_NO_CONTENT: None},
    exclude=True,
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([IvendPayApiKeyPermission])
def ivendpay_webhook(request: Request):
    gate = get_payment_gateway(gateway_type=GatewayType.ivendpay)

    data = json.loads(list(dict(request.data).keys())[0])

    qs = PaymentOrder.objects.filter(invoice_id=data['invoice'],
                                     gateway_type=gate.gateway_type,
                                     status=PaymentOrder.Status.CREATED)
    if order := qs.first():
        from apps.shop.gate.ivendpay import EXTERNAL_STATUSES
        gate.update(
            order=order,
            status=EXTERNAL_STATUSES.get(data['payment_status'], PaymentOrder.Status.ERROR),
            extra=dict(
                transaction_hash=data.get('hash'),
                explorer_url=data.get('explorer_url')
            ),
        )

    return Response(
        status=status.HTTP_204_NO_CONTENT,
    )


@extend_schema(
    request=OpenApiRequest(),
    responses={status.HTTP_204_NO_CONTENT: None},
    exclude=True,
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([PayAdmitSignaturePermission])
def payadmit_webhook(request: Request):
    gate = get_payment_gateway(gateway_type=GatewayType.payadmit)

    data = request.data

    qs = PaymentOrder.objects.select_related(
        'user', 'product',
    ).filter(invoice_id=data['id'],
             gateway_type=gate.gateway_type,
             status=PaymentOrder.Status.CREATED)
    if order := qs.first():
        from apps.shop.gate.payadmit import EXTERNAL_STATUSES
        gate.update(
            order=order,
            status=EXTERNAL_STATUSES.get(data['state'], PaymentOrder.Status.ERROR),
            extra=dict(
                amount=data.get('customerAmount'),
                currency=data.get('customerCurrency')
            ),
        )

    return Response(status=status.HTTP_200_OK)


@extend_schema(
    exclude=True,
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([ArkPayWebhookSignaturePermission])
def ark_pay_webhook(request: Request):
    from apps.shop.gate.ark_pay import EXTERNAL_STATUSES

    gate = get_payment_gateway(gateway_type=GatewayType.ark_pay)

    data = request.data
    with transaction.atomic():
        order = PaymentOrder.objects.select_for_update(
            nowait=True
        ).filter(
            invoice_id=data['id'],
            gateway_type=gate.gateway_type,
            status__in=[PaymentOrder.Status.CREATED,
                        PaymentOrder.Status.CANCEL],        # todo delete after fix
        ).first()

        if order and EXTERNAL_STATUSES.get(data['status']):
            gate.update(
                order=order,
                status=EXTERNAL_STATUSES[data['status']],
            )

    return Response(status=status.HTTP_200_OK)
