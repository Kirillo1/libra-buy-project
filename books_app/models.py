from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Жанр"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Book(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    author = models.CharField(
        max_length=100,
        verbose_name='Автор'
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name='Жанры'
    )
    description = models.TextField(
        max_length=500,
        verbose_name='Описание'
    )
    publication = models.CharField(
        max_length=100,
        verbose_name='Издательство'
    )
    publication_year = models.IntegerField(
        verbose_name='Год издания'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    image = models.ImageField(
        upload_to='books/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество'
    )
    seller = models.ForeignKey(
        User,
        related_name="books",
        on_delete=models.CASCADE,
        verbose_name="Продавец"
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Проверена администратором?'
    )

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        return ratings.aggregate(models.Avg('score'))['score__avg'] or 0
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="ratings", on_delete=models.CASCADE)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"