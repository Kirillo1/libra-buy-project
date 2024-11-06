from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Cart
from books_app.models import Book


@login_required(login_url='users:login')
def view_cart(request):
    cart_books = Cart.objects.all()

    context = {
        'cart_books': cart_books
    }

    return render(request, 'cart/cart.html', context)


@login_required
@require_POST
def add_to_cart(request):
    book_id = request.POST.get("book_id")
    if book_id:
        try:
            book = Book.objects.get(id=book_id)
            cart_item, created = Cart.objects.get_or_create(
                user=request.user, book=book)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return JsonResponse({"status": "success", "message": "Книга добавлена в корзину"})
        except Book.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Книга не найдена"})
    return JsonResponse({"status": "error", "message": "Некорректный запрос"})
