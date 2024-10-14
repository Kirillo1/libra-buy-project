from django.urls import path

from .views import view_books, view_detail_book


app_name = "books"

urlpatterns = [
    path('', view_books, name='index'),
    path('detail_book/<int:book_id>/', view_detail_book, name='detail_book')
]
