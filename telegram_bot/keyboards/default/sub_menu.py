"""Меню подписчика на бота."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


sub_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Список тем 📁"),
            KeyboardButton(text="Написать сообщение 📝"),
        ],
        [
            KeyboardButton(text="О нас 🧙 и проекте"),
        ],
    ],
    resize_keyboard=True,
)
