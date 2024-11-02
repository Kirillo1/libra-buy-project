from django.db import models
from django.contrib.auth import get_user_model

from books_app.models import Book


User = get_user_model()

class Comment(models.Model):
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comments',
        verbose_name='Автор'
    )
    email = models.EmailField(
        verbose_name='Email'
    )
    text = models.TextField(
        verbose_name='Комментарий'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Проверен администратором?'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.email} к книге "{self.book.name}"'
