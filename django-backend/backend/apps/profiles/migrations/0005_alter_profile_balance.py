# Generated by Django 3.2.22 on 2024-01-24 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_create_profile_subscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=25, verbose_name='Balance'),
        ),
    ]
