from django.urls import path

from .views import view_books


app_name = "books"

urlpatterns = [
    path('', view_books, name='index')
]
