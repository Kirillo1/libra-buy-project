from django.shortcuts import render, get_object_or_404, redirect

from .models import Book
from .forms import BookForm


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


def add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('books:index')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})


def edit_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:index')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/add_book.html', {'form': form})


def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    print(book)
    if request.method == 'POST':
        book.delete()
        return redirect('books:index')
    return render(request, 'books/delete_book.html', {'book': book})
