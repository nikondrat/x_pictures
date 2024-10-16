# Generated by Django 4.2.5 on 2023-10-16 14:55

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Price = apps.get_model('shop', 'Price')

    advance = Product.objects.create(
        id=1,
        title='Advance (Month)',
        public_title='Advance',
        type='subscription',
        lifetime=60 * 60 * 24 * 30,
        amount=100,
    )

    advance_week = Product.objects.create(
        id=2,
        title='Advance (Week)',
        public_title='Advance',
        type='subscription',
        lifetime=60 * 60 * 24 * 12,
        amount=100,
    )

    premium = Product.objects.create(
        id=3,
        title='Premium (Month)',
        public_title='Premium',
        type='subscription',
        lifetime=60 * 60 * 24 * 30,
        amount=200,
    )

    premium_week = Product.objects.create(
        id=4,
        title='Premium (Week)',
        public_title='Premium',
        type='subscription',
        lifetime=60 * 60 * 24 * 30,
        amount=200,
    )

    super_premium = Product.objects.create(
        id=5,
        title='Premium (12 months)',
        public_title='Premium',
        type='subscription',
        lifetime=60 * 60 * 24 * 30 * 12,
        amount=2400,
    )

    Price.objects.bulk_create([
        Price(id=1, currency='usd', price=10.9, product_id=advance.id),
        Price(id=2, currency='usd', price=6.9, product_id=advance_week.id),
        Price(id=3, currency='usd', price=17.9, product_id=premium.id),
        Price(id=4, currency='usd', price=9.9, product_id=premium_week.id),
        Price(id=5, currency='usd', price=99.9, product_id=super_premium.id),
    ])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
