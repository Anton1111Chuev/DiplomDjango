from django.contrib import admin
from .models import Product, CarModel, CarMark, Category, Manufacturer, Customer, Cart, CartProduct

# Register your models here.
admin.site.register(CarModel)
admin.site.register(Product)
admin.site.register(CarMark)
admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
