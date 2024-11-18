from rest_framework import serializers
from books_app.models import Book


class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = [
            'id', 'name', 'author',
            'description', 'publication',
            'publication_year', 'price',
            'image', 'quantity', 'seller',
            'create_at', 'is_verified',
            'average_rating'
        ]
