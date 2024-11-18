from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from books_app.models import Book
from .serializers import BookSerializer


@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    if not books.exists():
        return Response(
            {"detail": "No books found."},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def book_detail(request, pk):
    """
    Получить подробную информацию о книге по ее ID.
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(
            {"detail": "Книга не найдена."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = BookSerializer(book)
    return Response(serializer.data)
