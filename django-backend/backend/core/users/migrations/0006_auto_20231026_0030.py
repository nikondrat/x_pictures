# Generated by Django 3.2.22 on 2023-10-25 21:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_patreon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patreon',
            name='score',
        ),
        migrations.AddField(
            model_name='patreon',
            name='scope',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='scope'),
            preserve_default=False,
        ),
    ]
