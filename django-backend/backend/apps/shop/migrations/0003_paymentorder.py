# Generated by Django 3.2.22 on 2023-12-28 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0002_add_base_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(max_length=255, unique=True, verbose_name='Invoice ID')),
                ('payment_url', models.URLField(blank=True, default=None, null=True, verbose_name='Payment url')),
                ('price', models.DecimalField(decimal_places=2, max_digits=25, verbose_name='Price')),
                ('currency', models.CharField(choices=[('usd', 'USD'), ('rub', 'RUB')], default='usd', max_length=255, verbose_name='Currency')),
                ('gateway_type', models.CharField(choices=[('ivendpay', 'IvendPay'), ('paypal', 'PayPal'), ('paypal_subscription', 'PayPal (subscription)'), ('patreon', 'Patreon (subscription)'), ('payadmit', 'PayAdmit')], max_length=255, verbose_name='Gateway type')),
                ('status', models.IntegerField(choices=[(0, 'Created'), (1, 'Paid'), (-1, 'Cancel'), (-2, 'Error')], default=0, verbose_name='Status')),
                ('external_status', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='External status')),
                ('expiry_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Expiry At')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('extra', models.JSONField(blank=True, default=None, null=True, verbose_name='Extra data')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment_orders', to='shop.product', verbose_name='Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment_orders', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Payment order',
                'verbose_name_plural': 'Payment orders',
            },
        ),
    ]
