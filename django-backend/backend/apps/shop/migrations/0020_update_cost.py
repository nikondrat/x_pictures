# Generated by Django 4.2.5 on 2024-02-19
import decimal

from django.db import migrations, models


def update_product(pk: int,
                   price: decimal.Decimal,
                   amount: decimal.Decimal,
                   product_obj, price_obj,
                   public_title: str = None):
    product = product_obj.objects.get(pk=pk)
    product_price = price_obj.objects.get(product=product,
                                          currency='usd')
    if public_title:
        product.title = public_title
        product.public_title = public_title

    product.amount = amount
    product_price.price = price

    product.save()
    product_price.save()


def forwards_func(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Price = apps.get_model('shop', 'Price')

    # Subscription
    update_product(
        pk=2,  # Advance (week)
        amount=decimal.Decimal('280'),
        price=decimal.Decimal('10.9'),
        price_obj=Price, product_obj=Product,
    )
    update_product(
        pk=4,  # Premium (week)
        amount=decimal.Decimal('360'),
        price=decimal.Decimal('12.9'),
        price_obj=Price, product_obj=Product,
    )
    update_product(
        pk=1,  # Advance (month)
        amount=decimal.Decimal('900'),
        price=decimal.Decimal('14.9'),
        price_obj=Price, product_obj=Product,
    )
    update_product(
        pk=3,  # Premium (month)
        amount=decimal.Decimal('1200'),
        price=decimal.Decimal('17.9'),
        price_obj=Price, product_obj=Product,
    )
    update_product(
        pk=6,  # Advance (year)
        amount=decimal.Decimal('11000'),
        price=decimal.Decimal('124.9'),
        price_obj=Price, product_obj=Product,
    )
    update_product(
        pk=5,  # Premium (year)
        amount=decimal.Decimal('14900'),
        price=decimal.Decimal('139.9'),
        price_obj=Price, product_obj=Product,
    )
    update_product(
        pk=12,  # Premium (Special offer)
        amount=decimal.Decimal('1000'),
        price=decimal.Decimal('14.9'),
        price_obj=Price, product_obj=Product,
    )

    # Token
    update_product(
        pk=7,
        public_title='Tokens pack (100 pcs)',
        amount=decimal.Decimal('100'),
        price=decimal.Decimal('10.9'),
        price_obj=Price, product_obj=Product,
    )
    update_product(
        pk=8,
        public_title='Tokens pack (240 pcs)',
        amount=decimal.Decimal('240'),
        price=decimal.Decimal('12.9'),
        price_obj=Price, product_obj=Product,
    )
    update_product(
        pk=9,
        public_title='Tokens pack (350 pcs)',
        amount=decimal.Decimal('350'),
        price=decimal.Decimal('14.9'),
        price_obj=Price, product_obj=Product,
    )
    update_product(
        pk=10,
        public_title='Tokens pack (600 pcs)',
        amount=decimal.Decimal('600'),
        price=decimal.Decimal('24.9'),
        price_obj=Price, product_obj=Product,
    )
    update_product(
        pk=11,
        public_title='Tokens pack (1200 + 300 pcs)',
        amount=decimal.Decimal('1500'),
        price=decimal.Decimal('49.9'),
        price_obj=Price, product_obj=Product,
    )

    token_pack_3500_pcs = Product.objects.create(
        id=14,
        title='Tokens pack (3000 + 500 pcs)',
        public_title='Tokens pack (3000 + 500 pcs)',
        type='one-time',
        amount=3500,
        stripe_product_id='prod_PS7NQHHvksomzE',
    )
    Price.objects.create(
        id=14, currency='usd',
        price=99.9,
        product_id=token_pack_3500_pcs.id,
        stripe_price_id='price_1OdD8hDijmhB69Um6pAdUkEu'
    )

    update_product(
        pk=13,
        public_title='Tokens pack (32 pcs) (Special offer)',
        amount=decimal.Decimal('500'),
        price=decimal.Decimal('14.9'),
        price_obj=Price, product_obj=Product,
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('shop', '0019_alter_paymentorder_gateway_type'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
