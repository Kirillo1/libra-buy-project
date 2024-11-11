# from django.db import models
# from django.contrib.auth import get_user_model

# from books_app.models import Book

# User = get_user_model()


# class Order(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='orders'
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )
#     total_price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         verbose_name="Общая сумма",
#         default=0
#     )
#     address = models.CharField(
#         max_length=255,
#         verbose_name="Адрес доставки"
#     )
#     comment = models.TextField(
#         verbose_name='Комментарий'
#     )

#     class Meta:
#         verbose_name = "Заказ"
#         verbose_name_plural = "Заказы"

#     def __str__(self):
#         return f"Заказ {self.id} от {self.user.username}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(
#         Order,
#         on_delete=models.CASCADE,
#         related_name='order_items'
#     )
#     book = models.ForeignKey(
#         Book,
#         on_delete=models.CASCADE
#     )
#     quantity = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.book.name} (x{self.quantity})"
