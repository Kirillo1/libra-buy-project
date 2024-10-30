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
            comment.book_id = book_id
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()
            return redirect('books:detail_book', book_id=book.id)
    else:
        form = CommentForm()

    return redirect('books:detail_book', book_id=book.id)


def edit_comment_view(request, comment_id, book_id):
    comment = get_object_or_404(Comment, id=comment_id, book_id=book_id)
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('books:detail_book', book_id=book_id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comments/edit_comment.html', {'form': form, 'book': book, 'comment': comment})


def delete_comment_view(request, comment_id, book_id):
    comment = get_object_or_404(Comment, id=comment_id, book_id=book_id)
    comment.delete()
    return redirect('books:detail_book', book_id=book_id)
