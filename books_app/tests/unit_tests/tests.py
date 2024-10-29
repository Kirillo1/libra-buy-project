from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

from books_app.models import Book, Genre
from books_app.forms import BookForm
from books_app.views import (view_books, view_detail_book, 
                             add_book_view, edit_book_view, delete_book_view)

# Получение модели пользователя
User = get_user_model()

# Основной класс тестов для представлений книги
class BookViewTests(TestCase):
    # Установка начальных данных для тестов
    def setUp(self):
        # Инициализация фабрики запросов
        self.factory = RequestFactory()
        # Создание пользователя для тестов
        self.user = User.objects.create_user(username='testuser', password='password')
        # Создание жанра, который будет использоваться в книге
        self.genre = Genre.objects.create(name='Test Genre')
        # Создание тестовой книги
        self.book = Book.objects.create(
            name='Test Book',
            author='Test Author',
            description='Test Description',
            publication='Test Publication',
            publication_year=2023,
            price=100.00,
            seller=self.user
        )
        # Привязка жанра к книге
        self.book.genres.add(self.genre)

    # Тестирование представления списка книг
    def test_view_books(self):
        # Получение URL для представления списка книг
        url = reverse('books:index')
        # Выполнение GET-запроса
        response = self.client.get(url)
        # Проверка, что статус-код ответа равен 200
        self.assertEqual(response.status_code, 200)
        # Проверка использования правильного шаблона
        self.assertTemplateUsed(response, 'books/index.html')
        # Проверка, что список книг присутствует в контексте
        self.assertIn('books', response.context)
        # Проверка, что количество книг в контексте равно 1
        self.assertEqual(len(response.context['books']), 1)

    # Тестирование представления подробностей книги
    def test_view_detail_book(self):
        # Получение URL для страницы подробностей книги по её id
        url = reverse('books:detail_book', args=[self.book.id])
        # Выполнение GET-запроса
        response = self.client.get(url)
        # Проверка, что статус-код ответа равен 200
        self.assertEqual(response.status_code, 200)
        # Проверка использования правильного шаблона
        self.assertTemplateUsed(response, 'books/detail_book.html')
        # Проверка, что книга присутствует в контексте
        self.assertIn('book', response.context)
        # Проверка, что название книги в контексте совпадает с ожидаемым
        self.assertEqual(response.context['book'].name, 'Test Book')

    # Тестирование представления добавления книги (GET-запрос)
    def test_add_book_view_get(self):
        # Получение URL для представления добавления книги
        url = reverse('books:add_book')
        # Вход под тестовым пользователем
        self.client.login(username='testuser', password='password')
        # Выполнение GET-запроса
        response = self.client.get(url)
        # Проверка, что статус-код ответа равен 200
        self.assertEqual(response.status_code, 200)
        # Проверка использования правильного шаблона
        self.assertTemplateUsed(response, 'books/add_book.html')
        # Проверка, что форма книги присутствует в контексте
        self.assertIsInstance(response.context['form'], BookForm)

    # Тестирование представления добавления книги (POST-запрос)
    def test_add_book_view_post(self):
        # Получение URL для представления добавления книги
        url = reverse('books:add_book')
        # Данные для создания новой книги
        data = {
            'name': 'New Book',
            'author': 'New Author',
            'description': 'New Description',
            'publication': 'New Publication',
            'publication_year': 2023,
            'quantity': 10,
            'price': 200.00,
            'genres': [self.genre.id]
        }
        # Вход под тестовым пользователем
        self.client.login(username='testuser', password='password')
        # Выполнение POST-запроса с данными книги
        response = self.client.post(url, data)
        # Проверка, что статус-код ответа равен 302 (перенаправление)
        self.assertEqual(response.status_code, 302)
        # Проверка, что книга с названием 'New Book' была создана
        self.assertEqual(Book.objects.filter(name='New Book').count(), 1)

    # Тестирование представления редактирования книги (GET-запрос)
    def test_edit_book_view_get(self):
        # Получение URL для редактирования книги по её id
        url = reverse('books:edit_book', args=[self.book.id])
        # Вход под тестовым пользователем
        self.client.login(username='testuser', password='password')
        # Выполнение GET-запроса
        response = self.client.get(url)
        # Проверка, что статус-код ответа равен 200
        self.assertEqual(response.status_code, 200)
        # Проверка использования правильного шаблона
        self.assertTemplateUsed(response, 'books/add_book.html')
        # Проверка, что форма книги присутствует в контексте
        self.assertIsInstance(response.context['form'], BookForm)
        # Проверка, что форма редактирует правильный экземпляр книги
        self.assertEqual(response.context['form'].instance, self.book)

    # Тестирование представления редактирования книги (POST-запрос)
    def test_edit_book_view_post(self):
        # Получение URL для редактирования книги по её id
        url = reverse('books:edit_book', args=[self.book.id])
        # Данные для обновления книги
        data = {
            'name': 'Updated Book Name',
            'author': 'Test Author',
            'description': 'Test Description',
            'publication': 'Test Publication',
            'publication_year': 2023,
            'quantity': 10,
            'price': 150.00,
            'genres': [self.genre.id]
        }
        # Вход под тестовым пользователем
        self.client.login(username='testuser', password='password')
        # Выполнение POST-запроса с обновленными данными
        response = self.client.post(url, data)
        # Проверка, что статус-код ответа равен 302 (перенаправление)
        self.assertEqual(response.status_code, 302)
        # Обновление данных книги из базы данных
        self.book.refresh_from_db()
        # Проверка, что название книги обновилось
        self.assertEqual(self.book.name, 'Updated Book Name')

    # Тестирование представления удаления книги
    def test_delete_book_view(self):
        # Получение URL для удаления книги по её id
        url = reverse('books:delete_book', args=[self.book.id])
        # Вход под тестовым пользователем
        self.client.login(username='testuser', password='password')
        # Выполнение POST-запроса для удаления книги
        response = self.client.post(url)
        # Проверка, что статус-код ответа равен 302 (перенаправление)
        self.assertEqual(response.status_code, 302)
        # Проверка, что книга была удалена из базы данных
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

# Команда для запуска тестов
# python manage.py test books_app.tests.unit_tests.tests
