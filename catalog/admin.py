from django.contrib import admin

from .models import Category, Product, Customer, CartProduct, Cart, Order, Image

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Image)