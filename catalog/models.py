from decimal import Decimal

from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Category(models.Model):
    '''Категория кирпичей'''
    title = models.CharField(verbose_name='Заголовок', max_length=50)

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    '''Товар'''
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.TextField(verbose_name='Заголовок')
    images = models.ManyToManyField('Image', verbose_name='Фото', related_name='images')
    main_img = models.ForeignKey('Image', verbose_name='Главное фото', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Цена', decimal_places=0, max_digits=7)
    comment = models.CharField(verbose_name='Комметарий', max_length=255, null=True, blank=True)
    index = models.IntegerField(verbose_name='Порядок в очереди', default=10)

    def __str__(self):
        return f'{self.category.title} : {self.title}'

    def get_photo_url(self):
        return self.main_img.img.url


class Customer(models.Model):
    '''Клиент'''
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)
    session = models.TextField(
        verbose_name='Сессия пользователя', help_text='Используется у незарегистрированного пользователя')

    orders = models.ManyToManyField('Order', verbose_name='Заказы пользователя', null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Покупатель id={self.id}'


class CartProduct(models.Model):
    '''Продукт в корзине'''
    user = models.ForeignKey('Customer', verbose_name='Клиент', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')

    product = models.ForeignKey(Product, verbose_name="Кирпич", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Продукт корзины id={self.id}'


class Cart(models.Model):
    '''Корзина'''

    owner = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    final_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Общая цена', default=0)
    in_order = models.BooleanField(default=False)

    def __str__(self):
        return f'Корзина, id={self.id}'

    def recalculation(self, *args, **kwargs):
        '''Пересчет корзины'''
        self.final_price = Decimal(0)

        for cp in self.products.all():
            self.final_price += cp.product.price

        super().save(*args, **kwargs)


class Order(models.Model):
    '''Заказ'''
    name = models.CharField(verbose_name='Имя', max_length=30)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return f'Заявка id={self.id} {self.created_time.date()}'


class Image(models.Model):
    '''product image'''
    img = models.ImageField(verbose_name='photo')

    def __str__(self):
        return f'file - {self.img.name}'