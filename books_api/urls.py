from django.urls import path

from .views import book_list, book_detail


app_name = "books_api"

urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('book/<int:pk>/detail/', book_detail, name='book_detail')
]
