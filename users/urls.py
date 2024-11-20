from django.urls import path

from .views import (login_view, logout_view, view_admin_dashboard,
                    register_user_view, view_profile,
                    edit_profile_view, CustomPasswordChangeView)

app_name = "users"

urlpatterns = [
    path('profile/', view_profile, name='profile'),
    path('admin_dashboard/', view_admin_dashboard, name='admin_dashboard'),
    path('registration/', register_user_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
]
