# Generated by Django 5.0.1 on 2024-01-10 19:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partsapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Производитель')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='qty',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Количество'),
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='partsapp.manufacturer'),
        ),
    ]
