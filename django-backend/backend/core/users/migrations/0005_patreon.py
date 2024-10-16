# Generated by Django 3.2.22 on 2023-10-25 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_email_before_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patreon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255, verbose_name='Access token')),
                ('refresh_token', models.CharField(max_length=255, verbose_name='Refresh token')),
                ('expires_in', models.DateTimeField(verbose_name='Expires in')),
                ('score', models.CharField(max_length=255, verbose_name='Score')),
                ('token_type', models.CharField(default='Bearer', max_length=255, verbose_name='Token type')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='patreon', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Patreon',
                'verbose_name_plural': 'Patreon',
            },
        ),
    ]
