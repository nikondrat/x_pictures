from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from rest_framework import status, exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from drf_spectacular.utils import OpenApiParameter, extend_schema

from core.users.authentication import ApiTokenAuthentication
from apps.shop.models import GatewayType, PaymentOrder
from apps.shop.gate import get_payment_gateway
from apps.shop.rest import serializers


@extend_schema(
    parameters=[
        OpenApiParameter(name='token', required=True, description=_('PayPal token'), type=str),
        OpenApiParameter(name='action', required=True, description=_('Payment action'), type=str),
    ],
    request=None,
    responses={status.HTTP_302_FOUND: None},
    exclude=True,
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def paypal_callback(request: Request):
    action = request.query_params.get('action')
    invoice_id = request.query_params.get('token')

    if not invoice_id:
        raise exceptions.ValidationError({'token': _('Invoice id not found!')})
    if not action or action not in ('cancel', 'success'):
        raise exceptions.ValidationError({'action': _('Action not found!')})

    gate = get_payment_gateway(gateway_type=GatewayType.paypal)

    qs = PaymentOrder.objects.select_related(
        'user', 'product',
    ).filter(invoice_id=invoice_id,
             gateway_type=gate.gateway_type,
             status=PaymentOrder.Status.CREATED)

    redirect_url = settings.FRONT_SHOP_DOMAIN
    if order := qs.first():
        from apps.shop.gate.paypal import EXTERNAL_STATUSES
        order = gate.update(
            order=order,
            status=EXTERNAL_STATUSES[action],
        )
        redirect_url = gate.render_redirect_url(order=order)

    return HttpResponseRedirect(redirect_url)


@extend_schema(
    request=serializers.PayPalSubscriptionCallbackSerializer(),
    responses={status.HTTP_204_NO_CONTENT: None}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([ApiTokenAuthentication])
def paypal_subscription_callback(request: Request):
    serializer = serializers.PayPalSubscriptionCallbackSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    gate = get_payment_gateway(gateway_type=GatewayType.paypal_subscription)

    product, currency, plan_id = gate.get_product_by_subscription_id(
        subscription_id=serializer.validated_data['subscription_id']
    )

    gate.create(
        user=request.user,
        product=product,
        currency=currency,
        plan_id=plan_id,
        invoice_id=serializer.validated_data['invoice_id'],
        subscription_id=serializer.validated_data['subscription_id'],
    )

    return Response(
        status=status.HTTP_204_NO_CONTENT,
    )


@extend_schema(
    parameters=[
        OpenApiParameter(name='checkout_token', type=str, required=True),
    ],
    responses={status.HTTP_302_FOUND: None},
    exclude=True,
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def stripe_callback(request: Request):
    from apps.shop.gate.stripe import decode_checkout_token

    gate = get_payment_gateway(gateway_type=GatewayType.stripe)
    data = decode_checkout_token(checkout_token=request.query_params.get('checkout_token'))

    order = gate.update(
        order=PaymentOrder.objects.get(pk=data['pk']),
        status=PaymentOrder.Status(data['status']),
    )

    redirect_url = gate.render_redirect_url(order=order)

    return HttpResponseRedirect(redirect_url)


@extend_schema(
    request=serializers.EmoveganCallbackSerializer(),
    responses={status.HTTP_204_NO_CONTENT: None}
)
@api_view(['POST'])
@authentication_classes([ApiTokenAuthentication])
@permission_classes([IsAuthenticated])
def emovegan_callback(request: Request):
    from apps.shop.gate.emovegan import EXTERNAL_STATUSES
    serializer = serializers.EmoveganCallbackSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    current_status = EXTERNAL_STATUSES.get(serializer.validated_data['action'])

    order: PaymentOrder = PaymentOrder.objects.select_related(
        'user', 'product',
    ).filter(
        pk=serializer.validated_data['order_id'],
        user_id=request.user.pk,
        gateway_type=GatewayType.emovegan,
    ).first()
    if not order or order.is_confirmed or not current_status:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    gate = get_payment_gateway(gateway_type=GatewayType.emovegan)
    gate.update(
        order=order,
        status=current_status,
    )

    return Response(status=status.HTTP_204_NO_CONTENT)
