# Generated by Django 3.2.22 on 2024-01-22

from django.db import migrations, models
import django.db.models.deletion


def forwards_func(apps, schema_editor):
    SDModel = apps.get_model('jobs', 'SDModel')

    SDModel.objects.create(
        id=12,
        name='White Generate Model',
        public_name='White Generate Model',
        model_name='mbbxlUltimate_v10RC_94686.safetensors',
        type=0,
        raw_prompt='a art of',
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0022_auto_20240226_1819'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
