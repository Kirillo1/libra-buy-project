import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from decimal import Decimal

from .models import Order, OrderItem
from cart_app.models import Cart

@login_required(login_url='users:login')
def create_order(request):
    if request.method == "POST":
        address = request.POST.get("address")
        comment = request.POST.get("comment")
        user = request.user
        cart_books = Cart.objects.filter(user=user)

        if not cart_books.exists():
            messages.error(request, "Ваша корзина пуста.")
            return redirect('cart:cart')

        # Инициализируем общую стоимость
        total_price = Decimal(0)

        # Операции с базой данных будут атомарными, если внутри транзакции
        with transaction.atomic():
            # Создаем заказ
            order = Order.objects.create(
                user=user,
                address=address,
                comment=comment
            )

            # Перемещаем книги из корзины в заказ и рассчитываем общую сумму
            for cart_item in cart_books:
                book = cart_item.book

                if book.quantity < cart_item.quantity:
                    messages.error(request, f"Недостаточное количество книг: {book.name}")
                    transaction.set_rollback(True)
                    return redirect('cart:view_cart')

                # Создаем позиции заказа
                OrderItem.objects.create(
                    order=order,
                    book=book,
                    quantity=cart_item.quantity
                )

                # Уменьшаем количество книг на складе
                book.quantity -= cart_item.quantity
                book.save()

                # Рассчитываем общую сумму
                total_price += book.price * cart_item.quantity

            # Обновляем общую сумму в заказе
            order.total_price = total_price
            order.save()

            # Очищаем корзину
            cart_books.delete()

        messages.success(request, "Заказ успешно создан!")
        return redirect('books:index')

    return redirect('cart:view_cart')


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
@require_http_methods(["PATCH"])
def update_payment_status(request):
    data = json.loads(request.body)
    order_id = data.get("order_id")
    payment_status = data.get("payment_status")
    print(order_id)
    print(payment_status)

    try:
        order = Order.objects.get(id=order_id)
        order.payment_status = payment_status
        order.save()
        return JsonResponse({"status": "success"})
    except Order.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Заказ не найден"}
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
