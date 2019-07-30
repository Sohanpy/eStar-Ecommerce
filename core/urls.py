from django.urls import path

from .views import (
    ProductListView,
    DetailsView,
    Cart,
    add_to_cart,
    remove_signle_item_from_cart,
    remove_item_from_cart,
    clearcart,
    Checkout
)

app_name = 'core'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('detail/<slug>/', DetailsView.as_view(), name='detail'),
    path('cart/', Cart.as_view(), name='cart'),
    path('add-to-cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove-single/<slug>', remove_signle_item_from_cart,
         name='remove-single-item'),
    path('remove/<slug>', remove_item_from_cart,
         name='remove-item'),
    path('delete/', clearcart, name='delte'),
    path('checkout/', Checkout.as_view(), name='checkout')
]
