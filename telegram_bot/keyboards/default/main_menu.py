"""Главное меню бота."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Список тем 📁"),
            KeyboardButton(text="Добавить тему 📁"),
        ],
        [
            KeyboardButton(text="Список сообщений на конкретную тему 💬"),
            KeyboardButton(text="Список сообщений от корреспондента 👨‍⚕️"),
        ],
        [
            KeyboardButton(text="Количество сообщений в базе"),
            KeyboardButton(text="Количество подписчиков"),
        ],
        [
            KeyboardButton(text="О нас 🧙 и проекте"),
        ],
    ],
    resize_keyboard=True,
)
