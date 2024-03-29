# Generated by Django 5.0.1 on 2024-01-10 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Марка автомобиля')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Категория')),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Модель автомобиля')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('car_mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partsapp.carmark', verbose_name='Марка автомобиля')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена')),
                ('qty', models.PositiveIntegerField(blank=True, default=0, max_length=10, verbose_name='Количество')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Изображение')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('car_model', models.ManyToManyField(to='partsapp.carmodel', verbose_name='Модели')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partsapp.category', verbose_name='Категория')),
            ],
        ),
    ]
