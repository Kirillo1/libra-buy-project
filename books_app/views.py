from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Book
from .forms import BookForm

from comments_app.forms import CommentForm


def view_books(request):
    books = Book.objects.all()
    context = {
        "books": books
    }

    return render(request, "books/index.html", context=context)


def view_detail_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    genres = book.genres.all()
    comments = book.comments.all()
    form = CommentForm()

    context = {
        "book": book,
        "genres": genres,
        "comments": comments,
        "form": form,
    }
    return render(request, "books/detail_book.html", context=context)


@login_required(login_url='users:login')
def add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)  # Создаем объект книги, но не сохраняем его в базе данных
            book.seller = request.user  # Устанавливаем текущего пользователя как продавца
            book.save()  # Теперь сохраняем книгу в базе данных
            return redirect('books:index')  # Перенаправляем на нужную страницу
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})


@login_required(login_url='users:login')
def edit_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.seller != request.user:
        raise PermissionDenied(
            "У вас нет прав на редактирование этой книги."
    )

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:detail_book', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/add_book.html', {'form': form})


@login_required(login_url='users:login')
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.seller != request.user:
        raise PermissionDenied(
            "У вас нет прав на редактирование этой книги."
        )

    if request.method == 'POST':
        book.delete()
        return redirect('books:index')
    return render(request, 'books/delete_book.html', {'book': book})
