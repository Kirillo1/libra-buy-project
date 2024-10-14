from django.shortcuts import render

from .models import Book

def view_books(request):
    books = Book.objects.all()
    context = {
        "books": books
    }

    return render(request, "books/index.html", context=context)


def view_detail_book(request, book_id):
    book = Book.objects.get(id=book_id)
    context = {
        "book": book
    }
    return render(request, "books/detail_book.html", context=context)