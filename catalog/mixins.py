from django.views.generic import View
from .models import Customer, Cart


class CartMixin(View):
    '''Миксер корзины'''
    def dispatch(self, request, *args, **kwargs):
        if not self.request.session.get('user_id'):  # проверяем есть ли в сессии id юзера, если нет
            customer = Customer.objects.create(  # - значит создаем юзера и сесссию, сессия по
                # создаешь юзера по умолчанию хранится около 2 дней, поэтому пох, но можно поменять:
            )  # self.request.session.set_expiry[60] - 60 секунд хранится сессия
            self.request.session['user_id'] = customer.id
        else:
            customer = Customer.objects.filter(
                id=self.request.session.get('user_id')
            ).first()

        cart = Cart.objects.filter(owner=customer, in_order=False)
        if not cart:
            cart = Cart.objects.create(
                owner=customer,
                final_price=0
            )
        else:
            cart = cart.first()

        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
