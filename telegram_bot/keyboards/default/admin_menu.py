"""Меню администратора бота."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Список тем 📁"),
            KeyboardButton(text="Список корреспондентов 📁"),
            KeyboardButton(text="Добавить тему 📁"),
        ],
        [
            KeyboardButton(text="Список cообщений на конкретную тему 💬"),
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
