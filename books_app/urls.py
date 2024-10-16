from django.urls import path

from .views import (view_books, view_detail_book, 
                    add_book, delete_book, edit_book)


app_name = "books"

urlpatterns = [
    path('', view_books, name='index'),
    path('detail_book/<int:book_id>/', view_detail_book, name='detail_book'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', delete_book, name='delete_book')

]
