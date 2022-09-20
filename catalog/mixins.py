from django.views.generic import View
from .models import Customer, Cart


class CartMixin(View):
    '''Миксер корзины'''
    def dispatch(self, request, *args, **kwargs):
        customer = Customer.objects.filter(
            session=request.META['HTTP_USER_AGENT']
        ).first()

        if not customer:
            customer = Customer.objects.create(
                session=request.META['HTTP_USER_AGENT']
            )

        cart = Cart.objects.filter(owner=customer, in_order=False).first()
        if not cart:
            cart = Cart.objects.create(
                owner=customer,
                final_price=0,
            )

        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
