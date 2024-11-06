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


@require_POST
@login_required(login_url='users:login')
def add_to_cart(request):
    book_id = request.POST.get("book_id")
    try:
        book = Book.objects.get(id=book_id)

        if book.quantity == 0:
            return JsonResponse({"status": "error", "message": "В остатке нет книг"})

        cart_item, created = Cart.objects.get_or_create(
            user=request.user, book=book)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({"status": "success", "message": "Книга добавлена в корзину"})

    except Book.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Книга не найдена"})


@require_POST
@login_required(login_url='users:login')
def remove_from_cart(request):
    if request.method == "POST":
        cart_book_id = request.POST.get("cart_book_id")
        try:
            cart_book = Cart.objects.get(id=cart_book_id)
            cart_book.delete()
            return JsonResponse({"status": "success", "message": "Книга удалена из корзины."})
        except Cart.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Книга не найдена в корзине."})
    return JsonResponse({"status": "error", "message": "Некорректный запрос."})
