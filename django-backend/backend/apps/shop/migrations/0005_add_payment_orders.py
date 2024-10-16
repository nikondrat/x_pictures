# Generated by Django 4.2.5 on 2023-12-28 14:55
import json

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    PaymentOrder = apps.get_model('shop', 'PaymentOrder')

    Order = apps.get_model('payments', 'Order')
    IvendpayInvoice = apps.get_model('payments', 'IvendpayInvoice')
    PaypalInvoice = apps.get_model('payments', 'PaypalInvoice')
    PayPalSubscriptionInvoice = apps.get_model('payments', 'PayPalSubscriptionInvoice')
    PatreonSubscriptionInvoice = apps.get_model('payments', 'PatreonSubscriptionInvoice')
    PayAdmitInvoice = apps.get_model('payments', 'PayAdmitInvoice')

    payment_order_obj = []
    for order in Order.objects.filter(status=2):
        if order.product_id == 3:
            product_id = 3
        else:
            product_id = 5

        extra = {}
        sub_id = None
        if order.payment_type == 'ivendpay':
            invoice = IvendpayInvoice.objects.get(order_id=order.id)
            extra = {
                'crypto_currency': invoice.currency,
                'amount': invoice.amount,
                'transaction_hash': invoice.transaction_hash,
                'explorer_url': invoice.explorer_url,
            }
        elif order.payment_type == 'paypal_subscription':
            invoice = PayPalSubscriptionInvoice.objects.get(order_id=order.id)
            sub_id = invoice.subscription_id
            extra = {
                'billing_plan': invoice.billing_plan.id,
                'subscription_id': invoice.subscription_id,
            }
        elif order.payment_type == 'payadmit':
            invoice = PayAdmitInvoice.objects.get(order_id=order.id)
            extra = {
                'payment_method': invoice.payment_method,
                'amount': invoice.amount,
                'currency': invoice.currency,
            }
        elif order.payment_type == 'paypal':
            invoice = PaypalInvoice.objects.get(order_id=order.id)
        elif order.payment_type == 'patreon':
            invoice = PatreonSubscriptionInvoice.objects.get(order_id=order.id)
        else:
            continue

        payment_order_obj.append(PaymentOrder(
            id=order.id,
            sub_id=sub_id,
            invoice_id=invoice.invoice_id,
            payment_url=invoice.payment_url,
            user=order.user,
            product_id=product_id,
            price=order.amount,
            currency='usd',
            gateway_type=order.payment_type,
            status=1,
            external_status=invoice.status,
            expiry_at=getattr(invoice, 'expiry_at', None),
            extra=json.dumps(extra, default=str),
        ))

    PaymentOrder.objects.bulk_create(payment_order_obj)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0004_paymentorder_sub_id'),
        ('payments', '0012_auto_20231206_1245')
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
