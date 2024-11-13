from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponse, HttpRequest

from .models import Comment
from .forms import CommentForm
from books_app.models import Book


def add_comment_view(request: HttpRequest, book_id: int) -> HttpResponse:
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


def edit_comment_view(request: HttpRequest, comment_id: int, book_id: int) -> HttpResponse:
    comment = get_object_or_404(Comment, id=comment_id, book_id=book_id)
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('books:detail_book', book_id=book_id)
    else:
        form = CommentForm(instance=comment)

    return render(
        request, 'comments/edit_comment.html', {
            'form': form, 'book': book, 'comment': comment}
        )


def delete_comment_view(request: HttpRequest, comment_id: int, book_id: int) -> HttpResponse:
    comment = get_object_or_404(Comment, id=comment_id, book_id=book_id)
    comment.delete()
    return redirect('books:detail_book', book_id=book_id)


@require_POST
@user_passes_test(lambda u: u.is_superuser)  # Проверка: только для суперпользователей
def change_comment_status(request: HttpRequest, comment_id: int) -> JsonResponse:
    try:
        # Пытаемся найти комментарий с указанным ID
        comment = Comment.objects.get(id=comment_id)

        # Меняем статус is_verified на противоположный
        comment.is_verified = not comment.is_verified
        comment.save()

        # Возвращаем успешный ответ с обновленным статусом is_verified
        return JsonResponse(
            {"status": "success", "is_verified": comment.is_verified})
    except Comment.DoesNotExist:
        # Если комментарий не найден, возвращаем ошибку
        return JsonResponse(
            {"status": "error", "message": "Комментарий не найден"})
    except Exception as e:
        # Обрабатываем общую ошибку
        return JsonResponse({"status": "error", "message": str(e)})
