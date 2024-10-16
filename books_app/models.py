from django.db import models

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
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

