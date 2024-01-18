from django.db import models
from django.urls import reverse
from  django.contrib.auth import get_user_model

from partsapp.modules.services.utils import unique_slugify

User = get_user_model()

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Производитель')

    def __str__(self):
        return self.name


class Category(models.Model):
    NAME_ALL_CATEGORIES = "allcategories"

    name = models.CharField(max_length=255, blank=False, verbose_name='Категория')
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog', kwargs={'slug_cat': self.slug, 'slug_model': ActiveContext.active_model})


class CarMark(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Марка автомобиля')

    def __str__(self):
        return self.name


class CarModel(models.Model):
    NAME_ALL_MODELS = "allmodels"

    name = models.CharField(max_length=255, blank=False, verbose_name='Модель автомобиля')
    car_mark = models.ForeignKey(CarMark, on_delete=models.CASCADE, verbose_name='Марка автомобиля')
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse('catalog', kwargs={'slug_cat': ActiveContext.active_category, 'slug_model': self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Название')
    number = models.CharField(max_length=255, blank=True, verbose_name='Каталожный номер', null=True, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name='Описание', default='')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    qty = models.PositiveIntegerField(verbose_name='Количество', blank=True, default=0)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(upload_to='media/', null=True, blank=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, blank=True, null=True)
    car_model = models.ManyToManyField(CarModel, verbose_name='Модели')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug_product': self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class ActiveContext:
    active_category = Category.NAME_ALL_CATEGORIES
    active_model = CarModel.NAME_ALL_MODELS
    active_cart = None


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey('Product', verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(verbose_name='Количество', blank=False, default=1)
    final_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость')

    def __str__(self):
        return f'Продукт для корзины {self.product.name}'

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)