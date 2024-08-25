import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.users.models import User
from apps.subscriptions.models import Subscription


class OrderType(models.IntegerChoices):
    subscription = 0, _('Subscription')
    token = 1, _('Token')


class PaymentType(models.TextChoices):
    ivendpay = 'ivendpay', _('IvendPay')
    paypal = 'paypal', _('PayPal')
    paypal_subscription = 'paypal_subscription', _('PayPal (subscription)')
    patreon = 'patreon', _('Patreon (subscription)')
    payadmit = 'payadmit', _('PayAdmit')


class Order(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, _('Created')
        PAID = 2, _('Paid')
        CANCEL = -1, _('Cancel')
        ERROR = -2, _('Error')

    id = models.UUIDField(_('Order id'), default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='orders', on_delete=models.DO_NOTHING)
    product_id = models.IntegerField(_('Product ID'))

    type = models.IntegerField(_('Order type'), choices=OrderType.choices, default=OrderType.subscription)
    payment_type = models.CharField(_('Payment Type'), choices=PaymentType.choices, default=PaymentType.ivendpay,
                                    max_length=255)

    amount = models.DecimalField(_('Amount'), max_digits=25, decimal_places=2)
    fiat_currency = models.CharField(_('Fiat currency'), max_length=255)

    status = models.IntegerField(_('Status'), choices=Status.choices, default=Status.CREATED)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    _product = None

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'Order: {self.get_payment_type_display()}'

    @property
    def is_paid(self) -> bool:
        return self.status == self.Status.PAID

    @property
    def product_title(self) -> str:
        return self.product.title

    @property
    def invoice(self):
        cls_invoices = {
            PaymentType.ivendpay: IvendpayInvoice,
            PaymentType.paypal: PaypalInvoice,
            PaymentType.paypal_subscription: PayPalSubscriptionInvoice,
            PaymentType.patreon: PatreonSubscriptionInvoice,
            PaymentType.payadmit: PayAdmitInvoice
        }
        return cls_invoices[self.payment_type].objects.filter(order_id=self.pk).first()


class BaseInvoice(models.Model):
    order_id = models.UUIDField(_('Order ID'), default=uuid.uuid4, primary_key=True)
    invoice_id = models.CharField(_('Invoice id'), max_length=255, unique=True)
    payment_url = models.URLField(_('Payment url'))

    _order = None

    class Meta:
        abstract = True

    @property
    def order(self) -> Order:
        if not self._order:
            self._order = Order.objects.filter(pk=self.order_id).first()
        return self._order

    @property
    def created(self):
        return getattr(self.order, 'created', None)

    @property
    def updated(self):
        return getattr(self.order, 'updated', None)


class IvendpayInvoice(BaseInvoice):
    class Status(models.TextChoices):
        WAITING_FOR_PAYMENT = 'WAITING_FOR_PAYMENT', _('Waiting for payment')
        PAID = 'PAID', _('Paid')
        TIMEOUT = 'TIMEOUT', _('Timeout')
        CANCELED = 'CANCELED', _('Canceled')

    currency = models.CharField(_('Crypto currency'), max_length=255)
    amount = models.DecimalField(_('Crypto amount'), max_digits=25, decimal_places=18)
    status = models.CharField(_('Status'), choices=Status.choices, default=Status.WAITING_FOR_PAYMENT, max_length=255)

    transaction_hash = models.CharField(_('Transaction hash'), max_length=255, default=None, null=True, blank=True)
    explorer_url = models.URLField(_('Transaction hash'), default=None, null=True, blank=True)

    expiry_at = models.DateTimeField(_('Expiry At'))

    class Meta:
        verbose_name = _('IvendPay invoice')
        verbose_name_plural = _('IvendPay invoices')

    def __str__(self):
        return f'IvendPay: {self.invoice_id}'

    @property
    def is_expired(self):
        return timezone.now() >= self.expiry_at


class PayPalBillingPlan(models.Model):
    id = models.CharField(_('ID'), max_length=255, primary_key=True)

    product_id = models.CharField(_('ID'), max_length=255, help_text=_('ID in PayPal'))
    subscription = models.ForeignKey(Subscription, verbose_name=_('Product'), on_delete=models.CASCADE,
                                     related_name='billing_plans')

    fiat_currency = models.CharField(_('Fiat currency'), max_length=255)

    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('PayPal Billing Plan')
        verbose_name_plural = _('PayPal Billing Plans (subscription)')


class PaypalInvoice(BaseInvoice):
    class Status(models.TextChoices):
        CREATED = 'CREATED', _('Created')
        SUCCESS = 'SUCCESS', _('Success')
        CANCELED = 'CANCELED', _('Canceled')
        TIMEOUT = 'TIMEOUT', _('Timeout')

    status = models.CharField(_('Status'), choices=Status.choices, default=Status.CREATED, max_length=255)
    expiry_at = models.DateTimeField(_('Expiry At'), default=None, null=True)

    class Meta:
        verbose_name = _('PayPal invoice')
        verbose_name_plural = _('PayPal invoices')

    def __str__(self):
        return f'PayPal: {self.invoice_id}'

    @property
    def is_expired(self):
        return timezone.now() >= self.expiry_at


class PayPalSubscriptionInvoice(BaseInvoice):
    class Status(models.TextChoices):
        SUCCESS = 'SUCCESS', _('Success')

    payment_url = models.URLField(_('Payment url'), default=None, blank=True, null=True)
    billing_plan = models.ForeignKey(PayPalBillingPlan, verbose_name=_('Billing plan'), on_delete=models.DO_NOTHING,
                                     related_name='invoices')
    subscription_id = models.CharField(_('Subscription id'), max_length=255, help_text=_('PayPal subscription id'),
                                       default=None, null=True)
    status = models.CharField(_('Status'), choices=Status.choices, default=Status.SUCCESS, max_length=255)
    expiry_at = models.DateTimeField(_('Expiry At'), default=None, null=True)

    class Meta:
        verbose_name = _('PayPal Subscription invoice')
        verbose_name_plural = _('PayPal Subscription invoices')


class PatreonSubscriptionInvoice(BaseInvoice):
    class Status(models.TextChoices):
        PAID = 'PAID', _('Paid')

    payment_url = models.URLField(_('Payment url'), default=None, blank=True, null=True)
    status = models.CharField(_('Status'), choices=Status.choices, default=Status.PAID, max_length=255)
    expiry_at = models.DateTimeField(_('Expiry At'), default=None, null=True)

    class Meta:
        verbose_name = _('Patreon (subscription) invoice')
        verbose_name_plural = _('Patreon (subscription) invoices')


class PayAdmitInvoice(BaseInvoice):
    class Status(models.TextChoices):
        CREATED = 'CREATED', _('Created')
        PAID = 'PAID', _('Paid')
        CANCEL = 'CANCEL', _('Cancel')
        TIMEOUT = 'TIMEOUT', _('Timeout')
        ERROR = 'ERROR', _('Error')

    payment_url = models.URLField(_('Payment url'), default=None, blank=True, null=True)
    status = models.CharField(_('Status'), choices=Status.choices, default=Status.CREATED, max_length=255)
    payment_method = models.CharField(_('Payment method'), max_length=255, help_text=_('From PayAdmit'))

    amount = models.DecimalField(_('Amount'), max_digits=25, decimal_places=2, null=True, blank=True)
    currency = models.CharField(_('Currency'), max_length=255, null=True, blank=True)

    expiry_at = models.DateTimeField(_('Expiry At'), default=None, null=True)

    class Meta:
        verbose_name = _('PayAdmit invoice')
        verbose_name_plural = _('PayAdmit invoices')

    @property
    def is_expired(self):
        return timezone.now() >= self.expiry_at
