# Generated by Django 5.0.1 on 2024-01-17 20:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partsapp', '0005_remove_customer_adreess_cart_for_anonymous_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partsapp.product', verbose_name='Товар'),
        ),
    ]
