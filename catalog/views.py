from json import loads

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .models import Category, Product, Order, CartProduct
from .mixins import CartMixin


class CategoryView(CartMixin, View):
    '''Категории кирпича'''
    def get(self, request, *args, **kwargs):
        context = {
            'categories': Category.objects.all(),
            'product__1_1': Product.objects.get(id=7),
            'product__1_2': Product.objects.get(id=3),
            'product__1_3': Product.objects.get(id=4),
            'products': Product.objects.all().order_by('id'),
            'cart': self.cart
        }
        return render(request, 'index.html', context)


class ProductsSelectionView(CartMixin, View):
    '''Экран выбора кирпича'''
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(category__id=kwargs.get('category_id')).order_by('id')
        context = {
            'products': products ,
            'category': Category.objects.get(id=kwargs.get('category_id')),
            'categories': Category.objects.all(),
            'cart': self.cart
        }
        return render(request, 'category.html', context)


class ProductDetailView(CartMixin, View):
    '''Карточка кирпича'''
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs.get('product_id'))
        context = {'product': product,
                   'categories': Category.objects.all(),
                   'cart': self.cart
                   }
        return render(request, 'product.html', context)


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs.get('product_id'))
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        self.cart.recalculation()
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    '''Экран корзины'''
    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
            'categories': Category.objects.all(),
        }
        return render(request, 'cart.html', context)


class OrderView(CartMixin, View):
    '''Экран оформления заказа'''
    def get(self, request, *args, **kwargs):
        context = {
            'Order': Order,
            'cart': self.cart,
            'categories': Category.objects.all(),
        }
        return render(request, 'checkout.html', context)

    def post(self, request):
        data = loads(request.body)

        Order.objects.create(
            name=data['name'],
            cart=self.cart
        )
        self.cart.in_order = True
        self.cart.save()

        return JsonResponse({'status': 200})