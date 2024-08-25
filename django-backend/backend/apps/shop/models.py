import uuid
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.common.utils import PathAndRename
from core.common.mixins import ImageMixin
from core.users.models import User


class Currency(models.TextChoices):
    USD = 'usd', _('USD')
    RUB = 'rub', _('RUB')


class ProductType(models.TextChoices):
    subscription = 'subscription', _('Subscription')
    one_time = 'one-time', _('One time')


class Product(ImageMixin, models.Model):
    title = models.CharField(_('Title'), max_length=255)
    public_title = models.CharField(_('Public title'), max_length=255)

    description = models.TextField(_('Description'), default='')
    public_description = models.TextField(_('Public description'), default='')

    image = models.ImageField(_('Image'), upload_to=PathAndRename('products/'), null=True, blank=True, default=None)

    type = models.CharField(_('Type'), max_length=255, choices=ProductType.choices, default=ProductType.subscription)
    lifetime = models.IntegerField(_('Lifetime'), help_text=_('In second'), null=True, default=None, blank=True)
    amount = models.DecimalField(_('Amount'), decimal_places=2, max_digits=25)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)

    paypal_product_id = models.CharField(_('Paypal product id'), max_length=255, null=True, blank=True)
    stripe_product_id = models.CharField(_('Stripe product id'), max_length=255, null=True, blank=True)
    patreon_product_id = models.CharField(_('Patreon product id'), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title

    @property
    def td_lifetime(self):
        return timedelta(seconds=self.lifetime)

    @property
    def is_subscription(self) -> bool:
        return self.type == ProductType.subscription

    def get_price_obj(self, currency: Currency):
        return Price.objects.filter(product=self, currency=currency).first()

    def get_price_by_currency(self, currency: Currency):
        if obj := self.get_price_obj(currency=currency):
            return obj.price

    def get_paypal_billing_plan_id(self, currency: Currency):
        if obj := self.get_price_obj(currency=currency):
            return obj.paypal_billing_plan_id


class Price(models.Model):
    currency = models.CharField(_('Currency'), choices=Currency.choices, max_length=255)
    price = models.DecimalField(_('Amount'), decimal_places=2, max_digits=25)

    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE,
                                related_name='prices')

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)

    paypal_billing_plan_id = models.CharField(_('Paypal billing plan ID'), max_length=255, null=True, blank=True)
    stripe_price_id = models.CharField(_('Stripe price ID'), max_length=255, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'currency'],
                name='unique_price'),
        ]
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

    def __str__(self):
        return f'{self.product.title} {self.currency}'


class GatewayType(models.TextChoices):
    ivendpay = 'ivendpay', _('IvendPay')
    paypal = 'paypal', _('PayPal')
    paypal_subscription = 'paypal_subscription', _('PayPal (subscription)')
    patreon = 'patreon', _('Patreon (subscription)')
    payadmit = 'payadmit', _('PayAdmit')
    stripe = 'stripe', _('Stripe')
    emovegan = 'emovegan', _('Emovegan')
    ark_pay = 'ark_pay', _('ArkPay')


class PaymentOrder(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, _('Created')
        PAID = 1, _('Paid')
        CANCEL = -1, _('Cancel')
        ERROR = -2, _('Error')

    id = models.UUIDField(_('ID'), default=uuid.uuid4, primary_key=True)
    sub_id = models.CharField(_('Sub ID'), max_length=255, default=None, null=True, blank=True)
    invoice_id = models.CharField(_('Invoice ID'), max_length=500, unique=True)

    payment_url = models.URLField(_('Payment url'), max_length=500, default=None, blank=True, null=True)

    user = models.ForeignKey(User, verbose_name=_('User'), related_name='payment_orders',
                             on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='payment_orders',
                                on_delete=models.DO_NOTHING)

    price = models.DecimalField(_('Price'), max_digits=25, decimal_places=2)
    currency = models.CharField(_('Currency'), max_length=255, choices=Currency.choices, default=Currency.USD)
    gateway_type = models.CharField(_('Gateway type'), max_length=255, choices=GatewayType.choices)

    status = models.IntegerField(_('Status'), choices=Status.choices, default=Status.CREATED)
    external_status = models.CharField(_('External status'), max_length=255, default=None, blank=True, null=True)

    expiry_at = models.DateTimeField(_('Expiry At'), default=None, blank=True, null=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    extra = models.JSONField(_('Extra data'), default=None, blank=True, null=True)
    from_shop = models.BooleanField(_('From shop'), default=False)
    is_sent_email = models.BooleanField(_('Sent email'), default=False)

    class Meta:
        verbose_name = _('Payment order')
        verbose_name_plural = _('Payment orders')

    def __str__(self):
        return _('Order: {pk}').format(pk=self.pk)

    @property
    def is_expired(self):
        return not self.is_confirmed and timezone.now() >= self.expiry_at

    @property
    def is_paid(self) -> bool:
        return self.status == self.Status.PAID

    @property
    def is_confirmed(self) -> bool:
        return self.status != self.Status.CREATED

    @property
    def gateway(self):
        from apps.shop.gate import get_payment_gateway
        return get_payment_gateway(gateway_type=self.gateway_type)

    @property
    def book_name(self) -> str:
        books = {
            # Subscription
            2: _('The Art of Strategic Leadership: Mastering the Business Game'),
            4: _('Innovation Nation: Building a Culture of Creativity in Business'),
            1: _('The Power of Networking: Unlocking Opportunities for Business Success'),
            3: _('Financial Mastery: A Guide to Wealth and Business Prosperity'),
            12: _('Financial Mastery: A Guide to Wealth and Business Prosperity'),
            6: _("The Entrepreneur's Playbook: Strategies for Building a Thriving Business"),
            5: _('Leadership by Design: Crafting Your Path to Business Excellence'),
            # One time
            7: _('Managing Change: Adapting and Thriving in a Dynamic World'),
            8: _('Leadership Essentials: Key Principles for Effective Management'),
            9: _('Strategies for Organizational Growth: From Vision to Execution'),
            13: _('Strategies for Organizational Growth: From Vision to Execution'),
            10: _('Leading with Emotional Intelligence: Enhancing Leadership Skills'),
            11: _("The Manager's Guide to Productivity and Efficiency"),
        }
        return books[self.product_id]

    @property
    def book_pdf(self) -> str:
        books = {
            2: 'The Art of Strategic Leadership.pdf',
            4: 'Innovation_Nation_Building_a_Culture_of_Creativity_in_Business.pdf',
            1: 'The_Power_of_Networking_Unlocking_Opportunities_for_Business_Success.pdf',
            3: 'Financial Mastery- A Guide to Wealth and Business Prosperity.pdf',
            12: 'Financial Mastery- A Guide to Wealth and Business Prosperity.pdf',
            6: "The_Entrepreneur's_Playbook_Strategies_for_Building_a_Thriving_Business.pdf",
            5: 'Leadership_by_Design_Crafting_Your_Path_to_Business_Excellence.pdf',
        }

        if books.get(self.product_id):
            return settings.BOOKS_DIR / books[self.product_id]


class StripeCustomer(models.Model):
    id = models.CharField(_('ID'), max_length=255, primary_key=True)
    owner = models.OneToOneField(User, verbose_name=_('User'), on_delete=models.CASCADE,
                                 related_name='stripe_account')

    class Meta:
        verbose_name = _('Stripe customer')
        verbose_name_plural = _('Stripe customers')


class PaymentOrderLog(models.Model):
    class Action(models.TextChoices):
        INFO = 'INFO', _('Info')
        ERROR = 'ERROR', _('Error')

    order = models.ForeignKey(PaymentOrder, verbose_name=_('Payment Order'), related_name='log',
                              on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='order_logs',
                               null=True, blank=True, default=None,
                               on_delete=models.DO_NOTHING)

    action = models.CharField(_('Action'), max_length=20, choices=Action.choices,
                              default=Action.INFO)
    text = models.TextField(_('Text'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    class Meta:
        ordering = ['created', 'id']
        verbose_name = _('Payment order log')
        verbose_name_plural = _('Payment order logs')

    def __str__(self):
        return f'Payment order: {self.order_id} : {self.created.date()}'
