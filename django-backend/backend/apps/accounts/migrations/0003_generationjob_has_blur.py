# Generated by Django 3.2.22 on 2023-11-13 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_generationjob_created_alter_undressjob_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='generationjob',
            name='has_blur',
            field=models.BooleanField(default=False, verbose_name='Has blur'),
        ),
    ]
