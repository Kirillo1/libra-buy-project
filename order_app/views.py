# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db import transaction
# from decimal import Decimal

# from .models import Order, OrderItem
# from cart_app.models import Cart

# @login_required(login_url='users:login')
# def create_order(request):
#     if request.method == "POST":
#         address = request.POST.get("address")
#         comment = request.POST.get("comment")
#         user = request.user
#         cart_books = Cart.objects.filter(user=user)

#         if not cart_books.exists():
#             messages.error(request, "Ваша корзина пуста.")
#             return redirect('cart:cart')

#         # Инициализируем общую стоимость
#         total_price = Decimal(0)

#         # Операции с базой данных будут атомарными, если внутри транзакции
#         with transaction.atomic():
#             # Создаем заказ
#             order = Order.objects.create(
#                 user=user,
#                 address=address,
#                 comment=comment
#             )

#             # Перемещаем книги из корзины в заказ и рассчитываем общую сумму
#             for cart_item in cart_books:
#                 book = cart_item.book

#                 if book.quantity < cart_item.quantity:
#                     messages.error(request, f"Недостаточное количество книг: {book.name}")
#                     transaction.set_rollback(True)
#                     return redirect('cart:view_cart')

#                 # Создаем позиции заказа
#                 OrderItem.objects.create(
#                     order=order,
#                     book=book,
#                     quantity=cart_item.quantity
#                 )

#                 # Уменьшаем количество книг на складе
#                 book.quantity -= cart_item.quantity
#                 book.save()

#                 # Рассчитываем общую сумму
#                 total_price += book.price * cart_item.quantity

#             # Обновляем общую сумму в заказе
#             order.total_price = total_price
#             order.save()

#             # Очищаем корзину
#             cart_books.delete()

#         messages.success(request, "Заказ успешно создан!")
#         return redirect('books:index')

#     return redirect('cart:view_cart')