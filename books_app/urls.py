from django.urls import path

from .views import (view_books, view_detail_book, 
                    add_book_view, delete_book_view, edit_book_view,
                    change_book_status)


app_name = "books"

urlpatterns = [
    path('', view_books, name='index'),
    path('detail_book/<int:book_id>/', view_detail_book, name='detail_book'),
    path('add_book/', add_book_view, name='add_book'),
    path('edit_book/<int:book_id>/', edit_book_view, name='edit_book'),
    path('delete_book/<int:book_id>/', delete_book_view, name='delete_book'),
    path('change-book-status/<int:book_id>/', change_book_status, name='change_book_status'),
]
