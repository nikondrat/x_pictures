from django.utils.translation import gettext as _
from rest_framework import serializers, exceptions

from drf_spectacular.utils import extend_schema_field

from apps.shop import models
from apps.shop.rest import utils


class RequestProductSerializer(serializers.Serializer):
    create = update = None
    currency = serializers.ChoiceField(choices=models.Currency, default=models.Currency.USD, required=False)
    type = serializers.ChoiceField(choices=models.ProductType, default=models.ProductType.subscription, required=False)


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='public_title')
    description = serializers.CharField(source='public_description')
    price = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    lifetime_type = serializers.SerializerMethodField()
    paypal_billing_plan_id = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = (
            'id', 'title', 'description', 'image', 'price',
            'currency', 'type', 'amount', 'lifetime',
            'lifetime_type', 'paypal_billing_plan_id',
        )

    @extend_schema_field(serializers.CharField())
    def get_price(self, instance: models.Product):
        return str(instance.get_price_by_currency(currency=self.context['currency']) or 0.0)

    @extend_schema_field(serializers.ChoiceField(choices=models.Currency))
    def get_currency(self, _):
        return self.context['currency'].label

    @extend_schema_field(serializers.CharField(default=None, required=False,
                                               help_text=_('Only for subscription: week | month | year')))
    def get_lifetime_type(self, instance: models.Product):
        if instance.type == models.ProductType.subscription:
            match instance.pk:
                case 1 | 3:
                    return 'month'
                case 2 | 4:
                    return 'week'
                case 5 | 6:
                    return 'year'

    @extend_schema_field(serializers.CharField(default=None, required=False,
                                               help_text=_('For paypal button')))
    def get_paypal_billing_plan_id(self, instance: models.Product):
        return instance.get_paypal_billing_plan_id(currency=self.context['currency'])


class PaymentGatewaySerializer(serializers.Serializer):
    create = update = None

    id = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance: models.GatewayType):
        return {
            'id': instance.value,
            'label': instance.label,
        }


class CreatePaymentSerializer(serializers.Serializer):
    create = update = None

    gateway_id = serializers.ChoiceField(choices=models.GatewayType)
    currency = serializers.ChoiceField(choices=models.Currency)
    product_id = serializers.IntegerField()
    extra_data = serializers.DictField(required=False)

    def validate(self, attrs):
        try:
            attrs['product'] = models.Product.objects.get(pk=attrs['product_id'])
        except models.Product.DoesNotExist:
            raise exceptions.ValidationError({
                'product_id': _('Product not found!'),
            })

        if attrs['gateway_id'] not in utils.get_gateway_types_by_currency(currency=attrs['currency']):
            raise exceptions.ValidationError({
                'currency': _('The gateway is not suitable for this currency'),
            })

        return attrs


class PaymentOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    gateway = serializers.CharField(source='get_gateway_type_display')

    class Meta:
        model = models.PaymentOrder
        fields = (
            'id', 'payment_url', 'product',
            'price', 'currency', 'gateway',
            'status', 'expiry_at', 'created',
            'updated',
        )


class PayPalSubscriptionCallbackSerializer(serializers.Serializer):
    create = update = None
    invoice_id = serializers.CharField(label=_('Order ID in paypal data'))
    subscription_id = serializers.CharField(label=_('Subscription ID in paypal data'))


class EmoveganCallbackSerializer(serializers.Serializer):
    create = update = None
    action = serializers.CharField(label=_('Action'))
    order_id = serializers.UUIDField()
