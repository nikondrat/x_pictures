# Generated by Django 3.2.22 on 2024-07-11 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face2img', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lora',
            name='train_task_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Train task ID'),
        ),
    ]
