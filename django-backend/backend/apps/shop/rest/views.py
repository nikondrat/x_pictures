import uuid

from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import status, exceptions, mixins
from rest_framework.decorators import action, api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from drf_spectacular.utils import OpenApiParameter, extend_schema

from core.users.authentication import UserOrAnonymousAuthentication, ApiTokenAuthentication
from apps.shop import models
from apps.shop.rest import utils
from apps.shop.rest import serializers
from apps.shop.gate import get_payment_gateway
from apps.shop.rest.permissions import OnlyWithSubscriptionPermission
from apps.shop.rest.paginations import PaymentOrderPagination


@extend_schema(
    parameters=[
        OpenApiParameter(name='currency', required=False, default=models.Currency.USD, type=str),
    ],
    responses={status.HTTP_200_OK: serializers.ProductSerializer(many=True)},
    summary=_('Get products'),
    description=_('Get products'),
)
class ProductAPIViewSet(GenericViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        return models.Product.objects.filter()

    @action(methods=['GET'], detail=False, url_path='subscriptions', url_name='subscriptions')
    def get_subscription_products(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestProductSerializer(data={
            'type': models.ProductType.subscription,
            'currency': request.query_params.get('currency'),
        })
        serializer.is_valid(raise_exception=True)

        return Response(
            self.get_serializer(
                self.get_queryset().exclude(id=12).filter(type=serializer.validated_data['type']),
                many=True,
                context={'currency': serializer.validated_data['currency']}
            ).data
        )

    @action(methods=['GET'], detail=False, url_path='tokens', url_name='tokens')
    def get_one_time_products(self, request: Request, *args, **kwargs):
        serializer = serializers.RequestProductSerializer(data={
            'type': models.ProductType.one_time,
            'currency': request.query_params.get('currency'),
        })
        serializer.is_valid(raise_exception=True)

        return Response(
            self.get_serializer(
                self.get_queryset().exclude(id=13).filter(type=serializer.validated_data['type']),
                many=True,
                context={'currency': serializer.validated_data['currency']}
            ).data
        )


class PaymentAPIViewSet(GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin):
    authentication_classes = (UserOrAnonymousAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PaymentOrderPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name='currency', required=False, default=models.Currency.USD, type=str),
        ],
        responses={status.HTTP_200_OK: serializers.PaymentGatewaySerializer(many=True)},
        summary=_('Get payment gates'),
        description=_('Get payment gates'),
    )
    @action(methods=['GET'], detail=False, url_path='gates', url_name='gates')
    def get_payment_gateways(self, request: Request, *args, **kwargs):
        try:
            currency = models.Currency(request.query_params.get('currency', 'usd'))
        except ValueError:
            raise exceptions.ValidationError({
                'currency': _(f'Currency: `{request.query_params["currency"]}` not found!')
            })

        return Response(
            serializers.PaymentGatewaySerializer(
                utils.get_gateway_types_by_currency(currency=currency),
                many=True,
            ).data
        )

    @extend_schema(
        request=serializers.CreatePaymentSerializer,
        responses={status.HTTP_200_OK: serializers.PaymentOrderSerializer()},
        summary=_('Create payment order'),
        description=_('Create payment order'),
    )
    @action(methods=['POST'], detail=False, url_path='create-order', url_name='create_order')
    def create_payment_order(self, request: Request, *args, **kwargs):
        serializer = serializers.CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        gate = get_payment_gateway(gateway_type=serializer.validated_data['gateway_id'])

        options = serializer.validated_data.get('extra_data') or {}
        order = gate.create(
            user=request.user,
            product=serializer.validated_data['product'],
            currency=serializer.validated_data['currency'],
            **options,
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializers.PaymentOrderSerializer(
                order,
                context={'currency': serializer.validated_data['currency']}
            ).data,
        )

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='id', location=OpenApiParameter.PATH, required=True, type=uuid.UUID)
        ],
        responses={
            status.HTTP_200_OK: serializers.PaymentOrderSerializer(),
        },
        summary=_('Payment order detail'),
        description=_('Payment order detail'),
    )
    def retrieve(self, request: Request, *args, **kwargs):
        if request.user.is_anonymous:
            raise exceptions.PermissionDenied(_('You do not have permission to view this page'))

        order: models.PaymentOrder = models.PaymentOrder.objects.select_related(
            'product',
        ).filter(
            pk=kwargs['pk'],
            user_id=request.user.pk,
        ).first()
        if not order:
            raise exceptions.NotFound(_('Order not found!'))

        return Response(
            status=status.HTTP_200_OK,
            data=serializers.PaymentOrderSerializer(
                order,
                context={'currency': models.Currency(order.currency)}
            ).data,
        )

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='currency', required=False, default=models.Currency.USD, type=str),
        ],
        responses={
            status.HTTP_200_OK: serializers.PaymentOrderSerializer(many=True),
        },
        summary=_('Payment orders'),
        description=_('Payment orders'),
    )
    def list(self, request: Request, *args, **kwargs):
        if request.user.is_anonymous:
            raise exceptions.PermissionDenied(_('You do not have permission to view this page'))

        try:
            currency = models.Currency(request.query_params.get('currency', 'usd'))
        except ValueError:
            raise exceptions.ValidationError({
                'currency': _(f'Currency: `{request.query_params["currency"]}` not found!')
            })

        qs = models.PaymentOrder.objects.select_related(
            'product',
        ).filter(user_id=request.user.pk, currency=currency)

        page = self.paginate_queryset(qs)

        return self.get_paginated_response(
            serializers.PaymentOrderSerializer(
                page,
                context={'currency': currency},
                many=True,
            ).data
        )


@extend_schema(
    request=None,
    responses={status.HTTP_204_NO_CONTENT: None},
    summary=_('Disable subscription'),
    description=_('Disable subscription'),
)
@api_view(['POST'])
@authentication_classes([ApiTokenAuthentication])
@permission_classes([OnlyWithSubscriptionPermission])
def cancel_subscription(request: Request):
    utils.cancel_subscription(
        user=request.user,
    )
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    request=serializers.CreatePaymentSerializer,
    responses={status.HTTP_200_OK: serializers.PaymentOrderSerializer()},
    summary=_('Create payment order for shop'),
    description=_('Create payment order for shop'),
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def create_order_for_shop(request: Request):
    from core.users.models import User, generate_user_id

    serializer = serializers.CreatePaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    gate = get_payment_gateway(gateway_type=serializer.validated_data['gateway_id'])

    options = serializer.validated_data.get('extra_data') or {}

    user, _ = User.objects.get_or_create(
        email=options.pop('email'),
        defaults=dict(
            id=generate_user_id(),
            decoded_password=settings.SOCIAL_SECRET,
            auth_provider=User.AuthProvider.shop,
            email_confirmed=True,
        )
    )
    user.set_password(raw_password=settings.SOCIAL_SECRET)
    user.save()

    order = gate.create(
        user=user,
        product=serializer.validated_data['product'],
        currency=serializer.validated_data['currency'],
        from_shop=True,
        **options,
    )

    return Response(
        status=status.HTTP_201_CREATED,
        data=serializers.PaymentOrderSerializer(
            order,
            context={'currency': serializer.validated_data['currency']}
        ).data,
    )
