"""Кнопка отмены в меню при заполнении заявок."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌Отменить"),
        ],
    ],
    resize_keyboard=True,
)
