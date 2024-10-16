from django.shortcuts import render, get_object_or_404

from .models import Book

def view_books(request):
    books = Book.objects.all()
    context = {
        "books": books
    }

    return render(request, "books/index.html", context=context)


def view_detail_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    genres = book.genres.all()
    context = {
        "book": book,
        "genres": genres
    }
    return render(request, "books/detail_book.html", context=context)