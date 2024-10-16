# Generated by Django 3.2.22 on 2024-03-14 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_update_balances'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patreon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255, verbose_name='Access token')),
                ('refresh_token', models.CharField(max_length=255, verbose_name='Refresh token')),
                ('expires_in', models.DateTimeField(verbose_name='Expires in')),
                ('scope', models.CharField(max_length=255, verbose_name='scope')),
                ('token_type', models.CharField(default='Bearer', max_length=255, verbose_name='Token type')),
                ('patreon_id', models.IntegerField(blank=True, default=None, null=True, verbose_name='Patreon ID')),
                ('member_id', models.UUIDField(blank=True, default=None, null=True, verbose_name='Member ID')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patreon', to='profiles.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Patreon',
                'verbose_name_plural': 'Patreon',
            },
        ),
    ]
