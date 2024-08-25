from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext as _

from rangefilter.filters import DateTimeRangeFilterBuilder

from apps.shop import models


class PriceInline(admin.StackedInline):
    model = models.Price
    extra = 1
    min_num = 1
    max_num = 5


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'preview_image_tag')
    list_filter = ('type',)
    readonly_fields = ('image_tag',)
    exclude = ('prices',)
    inlines = (PriceInline,)


@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    list_select_related = ('product',)
    raw_id_fields = ('product',)
    list_display = ('id', 'product', 'price', 'currency')
    list_filter = ('currency', 'product')


class PaymentOrderLogInline(admin.TabularInline):
    model = models.PaymentOrderLog
    raw_id_fields = ('author',)
    fields = ('action', 'text', 'created')
    readonly_fields = ('id', 'author', 'action', 'text', 'created')
    extra = 0


@admin.register(models.PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'email', 'product', 'gateway_type', 'status', 'is_sent_email', 'created')
    list_filter = (
        ('created', DateTimeRangeFilterBuilder(
            title=_('Created'),
            default_start=timezone.now() - timezone.timedelta(days=1),
            default_end=timezone.now()
        )),
        'gateway_type', 'status',
    )
    ordering = (
        '-created',
        'status',
    )
    raw_id_fields = (
        'user', 'product',
    )
    search_fields = ('id', 'sub_id', 'invoice_id', 'user__id', 'user__email')
    readonly_fields = (
        'id', 'user', 'created', 'updated',
        'gateway_type', 'extra',
        'external_status', 'payment_url',
        'invoice_id', 'price', 'currency',
        'product',
    )
    exclude = ('order_logs',)
    inlines = [PaymentOrderLogInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product')

    @admin.display(ordering='profile__owner__email', description='Email')
    def email(self, obj: models.PaymentOrder):
        return obj.user.email


@admin.register(models.PaymentOrderLog)
class PaymentOrderLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'action', 'created')
    search_fields = ('id', 'order_id')
    list_filter = ('action',)
    raw_id_fields = ('order', 'author')
