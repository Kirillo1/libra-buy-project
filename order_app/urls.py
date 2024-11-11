from django.urls import path

from .views import create_order, update_payment_status

app_name = "order"

urlpatterns = [
    path('create_order/', create_order, name='create_order'),
    path("update_payment_status/", update_payment_status, name="update_payment_status"),

]