from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from books_app.models import Book

User = get_user_model()


class UserViewTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser', password='password')
        # Создаем тестовую книгу
        self.book = Book.objects.create(
            name='Test Book',
            author='Test Author',
            description='Test Description',
            publication='Test Publication',
            publication_year=2023,
            quantity=10,
            price=100.00,
            seller=self.user
        )

    def test_view_profile_authenticated(self):
        # Авторизуем пользователя и проверяем доступ к профилю
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIn('user_books', response.context)
        self.assertEqual(len(response.context['user_books']), 1)

    def test_view_profile_unauthenticated(self):
        # Проверяем, что неавторизованный пользователь перенаправляется на страницу входа
        response = self.client.get(reverse('users:profile'))
        self.assertRedirects(response, reverse(
            'users:login') + '?next=' + reverse('users:profile'))

    def test_register_user_view(self):
        # Проверяем, что регистрация пользователя работает корректно
        url = reverse('users:registration')
        data = {
            'username': 'newuser',
            'first_name': 'testUser',
            'last_name': 'testLastName',
            'father_name': 'testFatherName',
            'email': 'test_mail@gmail.com',
            'phone_number': '+79334421134',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(url, data)
        # print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('books:index'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_success(self):
        # Проверяем успешный вход
        url = reverse('users:login')
        data = {
            'username': 'testuser',
            'password': 'password'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('books:index'))

    def test_login_view_failure(self):
        # Проверяем неуспешный вход при неправильных данных
        url = reverse('users:login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_logout_view(self):
        # Проверяем успешный выход из системы
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('books:index'))


# python manage.py test users.tests.unit_tests.tests
