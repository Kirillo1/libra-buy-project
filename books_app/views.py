from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Book, Rating
from .forms import BookForm

from comments_app.forms import CommentForm


def view_books(request):
    books_list = Book.objects.all()
    paginator = Paginator(books_list, 12)  # Показывает 8 книг на странице

    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

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


@require_POST
@user_passes_test(lambda u: u.is_superuser)  # Проверка: только для суперпользователей
def change_book_status(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        # Меняем статус на противоположный
        book.is_verified = not book.is_verified
        book.save()
        return JsonResponse({"status": "success", "is_verified": book.is_verified})
    except Book.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Книга не найдена"})


@login_required(login_url='users:login')
def rate_book(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        score = int(request.POST.get("score"))

        # Убедимся, что оценка в пределах 1-5
        if score < 1 or score > 5:
            return JsonResponse({"status": "error", "message": "Что то пошло не так"})

        # Обновляем или создаем оценку
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={"score": score}
        )

        # Пересчитываем средний рейтинг
        average_rating = book.average_rating

        return JsonResponse({"status": "success", "average_rating": average_rating})
    return JsonResponse({"status": "error", "message": "Только POST запросы разрешены."})