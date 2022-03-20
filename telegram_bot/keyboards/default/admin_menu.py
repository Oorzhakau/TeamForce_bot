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
            KeyboardButton(text="Отправить сообщение корреспонденту(-ам)📩"),
            KeyboardButton(text="Рассылка группе пользователей 📩"),
        ],
        [
            KeyboardButton(text="Количество сообщений в базе"),
            KeyboardButton(text="Ссылка на бота"),
        ],
    ],
    resize_keyboard=True,
)
