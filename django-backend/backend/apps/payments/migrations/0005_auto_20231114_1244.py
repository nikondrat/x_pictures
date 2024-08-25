# Generated by Django 3.2.22 on 2023-11-14 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20231113_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='paypalinvoice',
            name='expiry_at',
            field=models.DateTimeField(default=None, null=True, verbose_name='Expiry At'),
        ),
        migrations.AlterField(
            model_name='paypalinvoice',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('SUCCESS', 'Success'), ('CANCELED', 'Canceled'), ('TIMEOUT', 'Timeout')], default='CREATED', max_length=255, verbose_name='Status'),
        ),
    ]
