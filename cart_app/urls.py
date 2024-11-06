from django.urls import path

from .views import view_cart, add_to_cart


app_name = "cart"

urlpatterns = [
    path('cart/', view_cart, name='cart'),
    path("cart/add_to_cart/", add_to_cart, name="add_to_cart"),

]