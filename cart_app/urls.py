from django.urls import path

from .views import view_cart


app_name = "cart"

urlpatterns = [
    path('cart/', view_cart, name='cart'),
]