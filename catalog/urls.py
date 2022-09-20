from django.urls import path

from .views import CategoryView, ProductsSelectionView, ProductDetailView, \
    AddToCartView, CartView, OrderView

urlpatterns = [
    path('', CategoryView.as_view(), name='main_catalog'),
    path('products_selection/<str:category_id>/', ProductsSelectionView.as_view(), name='products_selection'),
    path('products_detail/<str:product_id>/', ProductDetailView.as_view(), name='products_detail'),
    path('add_to_cart/<str:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('order/', OrderView.as_view(), name='order_view'),

]