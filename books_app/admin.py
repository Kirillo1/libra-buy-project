from django.contrib import admin

from .models import Book, Genre, Rating


admin.site.register(Book)

admin.site.register(Genre)

admin.site.register(Rating)

