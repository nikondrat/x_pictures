# Generated by Django 3.2.22 on 2024-01-07 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_add_payment_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='paypal_billing_plan_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Paypal billing plan ID'),
        ),
        migrations.AddField(
            model_name='price',
            name='stripe_price_id',
            field=models.CharField(max_length=255, null=True, verbose_name='Stripe price ID'),
        ),
        migrations.AddField(
            model_name='product',
            name='paypal_product_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Paypal product id'),
        ),
        migrations.AddField(
            model_name='product',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Stripe product id'),
        ),
        migrations.AlterField(
            model_name='paymentorder',
            name='gateway_type',
            field=models.CharField(choices=[('ivendpay', 'IvendPay'), ('paypal', 'PayPal'), ('paypal_subscription', 'PayPal (subscription)'), ('patreon', 'Patreon (subscription)'), ('payadmit', 'PayAdmit'), ('stripe', 'Stripe')], max_length=255, verbose_name='Gateway type'),
        ),
    ]
