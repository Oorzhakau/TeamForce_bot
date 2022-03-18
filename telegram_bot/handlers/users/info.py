from aiogram import types
import logging

from filters.filters_admin import IsAdmin
from loader import dp
from utils.db_api import db_commands as commands
from aiogram.dispatcher.filters import Text


@dp.message_handler(IsAdmin(), text="Количество подписчиков")
async def bot_message(message: types.Message):
    '''handler для получения количества подписчиков в базе'''
    await message.answer(
        f"Количество подписчиков - "
        + f"<b>{await commands.get_count_subscribers()}</b>"
    )
    logging.info("Запрос количества подписчиков.")


@dp.message_handler(IsAdmin(), text="Количество сообщений в базе")
async def bot_message(message: types.Message):
    '''handler для получения количества сообщений в базе'''
    await message.answer(
        "Количество сообщений в базе - "
        + f"<b>{await commands.get_count_messages()}</b>"
    )
    logging.info("Запрос количества сообщений в базе.")
