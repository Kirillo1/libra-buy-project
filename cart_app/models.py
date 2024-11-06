from django.db import models
from django.contrib.auth import get_user_model

from books_app.models import Book


User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        unique_together = ('user', 'book')
        verbose_name = "КОрзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"{self.user.username} - {self.book.name} (x{self.quantity})"
