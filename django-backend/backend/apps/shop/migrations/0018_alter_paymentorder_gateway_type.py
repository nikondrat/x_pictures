# Generated by Django 3.2.22 on 2024-02-13 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_fake_logs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentorder',
            name='gateway_type',
            field=models.CharField(choices=[('ivendpay', 'IvendPay'), ('paypal', 'PayPal'), ('paypal_subscription', 'PayPal (subscription)'), ('patreon', 'Patreon (subscription)'), ('payadmit', 'PayAdmit'), ('stripe', 'Stripe'), ('emovegan', 'Emovegan')], max_length=255, verbose_name='Gateway type'),
        ),
    ]
