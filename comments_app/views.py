from django.shortcuts import get_object_or_404, redirect, render
from .models import Comment
from .forms import CommentForm
from books_app.models import Book


def add_comment_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.save()
            return redirect('books:detail_book', book_id=book.id)
    else:
        form = CommentForm()

    return redirect('books:detail_book', book_id=book.id)
