import asyncio
import os
from os import getenv
from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)
from aiogram.filters import Command as Com
from django.core.management.base import BaseCommand
from books_app.models import Book

TELEGRAM_API_TOKEN = getenv("TG_BOT_TOKEN")
# Разрешение асинхронных операций с Django, так как Aiogram работает с асинхронным кодом
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


# Функция для получения всех книг из базы данных Django (параллельный доступ к базе)
@sync_to_async
def get_books():
    return Book.objects.all()


# Команда для запуска бота через Django management command
class Command(BaseCommand):
    help = "Запуск Telegram бота"

    # Метод, который вызывается при запуске команды
    def handle(self, *args, **kwargs):
        asyncio.run(run_bot())  # Запускаем асинхронную функцию для старта бота


# Функция для создания клавиатуры с кнопками для всех книг
async def create_books_keyboard() -> InlineKeyboardMarkup:
    books = await get_books()  # Получаем все книги
    inline_keyboard = []

    # Для каждой книги создаем кнопку с ее названием
    for book in books:
        button = InlineKeyboardButton(
            text=book.name,  # Текст на кнопке — название книги
            callback_data=f"book_{book.id}"  # Данные для обработки при нажатии
        )
        inline_keyboard.append([button])  # Добавляем кнопку в список

    # Создаем и возвращаем клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard


# Обработчик команды "/start", который вызывается при старте бота
async def start_command(message: Message):
    keyboard = await create_books_keyboard()  # Создаем клавиатуру с книгами
    await message.answer(
        "Выберите любую книгу для просмотра информации о ней",  # Сообщение для пользователя
        reply_markup=keyboard  # Прикрепляем клавиатуру
    )


# Обработчик нажатия на книгу для показа деталей
async def book_details(callback_query: CallbackQuery):
    book_id = int(callback_query.data.split("_")[-1])  # Извлекаем ID книги из данных callback
    books = await get_books()  # Получаем все книги
    book = next((b for b in books if b.id == book_id), None)  # Находим книгу по ID

    # Если книга найдена
    if book:
        # Создаем клавиатуру с кнопкой "Назад"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="Назад", callback_data="back_to_main")]  # Кнопка для возврата в меню
            ]
        )
        # Отправляем информацию о книге с кнопкой "Назад"
        await callback_query.message.edit_text(
            f"Название: {book.name}\n"
            f"Автор: {book.author}\n"
            f"Описание: {book.description}\n"
            f"Рейтинг: {book.ratings}\n"
            f"Цена: {book.price}",
            reply_markup=keyboard  # Прикрепляем клавиатуру с кнопкой "Назад"
        )
    else:
        await callback_query.message.edit_text("Книга не найдена.")  # Если книга не найдена
    await callback_query.answer()  # Завершаем обработку запроса


# Обработчик для кнопки "Назад", который возвращает пользователя в главное меню
async def back_to_main_menu(callback_query: CallbackQuery):
    keyboard = await create_books_keyboard()  # Создаем клавиатуру с книгами
    # Отправляем сообщение с предложением выбрать книгу из списка
    await callback_query.message.edit_text(
        "Выберите любую книгу для просмотра информации о ней",
        reply_markup=keyboard  # Прикрепляем клавиатуру
    )
    await callback_query.answer()  # Завершаем обработку запроса


# Главная асинхронная функция для запуска бота
async def run_bot():
    bot = Bot(token=TELEGRAM_API_TOKEN)  # Инициализируем бота с токеном
    dp = Dispatcher()  # Создаем диспетчер для обработки обновлений

    # Регистрируем обработчик для команды "/start"
    dp.message.register(start_command, Com(commands=["start"]))
    # Регистрируем обработчик для нажатий на книги
    dp.callback_query.register(
        book_details, lambda c: c.data.startswith("book_"))
    # Регистрируем обработчик для кнопки "Назад"
    dp.callback_query.register(
        back_to_main_menu, lambda c: c.data == "back_to_main")

    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    try:
        await dp.start_polling(bot)  # Запуск опроса обновлений
    finally:
        await bot.session.close()  # Закрываем сессию при завершении работы
