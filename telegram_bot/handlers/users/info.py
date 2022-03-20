from aiogram import types

from filters.filters_admin import IsAdmin
from loader import dp
from utils.db_api import db_commands as commands


@dp.message_handler(IsAdmin(), text="Количество подписчиков")
async def bot_message_count_subsribers(message: types.Message):
    """handler для получения количества подписчиков в базе"""
    await message.answer(
        "Количество подписчиков - "
        + f"<b>{await commands.get_count_subscribers()}</b>"
    )


@dp.message_handler(IsAdmin(), text="Количество сообщений в базе")
async def bot_message_count_message(message: types.Message):
    """handler для получения количества сообщений в базе"""
    await message.answer(
        "Количество сообщений в базе - "
        + f"<b>{await commands.get_count_messages()}</b>"
    )
