from django.urls import path

from .views import login_view, logout_view, register_user_view

app_name = "users"

urlpatterns = [
    path('registration', register_user_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
