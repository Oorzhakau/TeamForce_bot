from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .callback_datas import message_callback, tag_callback, sub_callback


message_choices = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Удалить",
            callback_data=message_callback.new(operation="delete")
        ),
        InlineKeyboardButton(
            text="Просмотрено",
            callback_data=message_callback.new(operation="complite"))
    ],
])


tag_choices = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Удалить",
            callback_data=tag_callback.new(operation="delete")
        ),
    ],
])