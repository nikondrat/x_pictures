# Generated by Django 3.2.22 on 2023-11-21 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support', '0003_auto_20231121_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supportmessage',
            options={'verbose_name': 'Support message', 'verbose_name_plural': 'Support messages'},
        ),
        migrations.CreateModel(
            name='SupportAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Message')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='answers', to='support.supportmessage', verbose_name='Message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_answers', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Support answer',
                'verbose_name_plural': 'Support answers',
            },
        ),
    ]
