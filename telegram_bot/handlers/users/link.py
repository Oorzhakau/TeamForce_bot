import asyncio
import os

from aiogram import types

from loader import dp
from utils.db_api import db_commands as commands

loop = asyncio.get_event_loop()
coroutine = commands.get_user()
User = loop.run_until_complete(coroutine)


@dp.message_handler(text="Ссылка на бота")
async def bot_message(message: types.Message):
    """handler для отправки ссылки на бота"""
    bot_name = os.environ.get("BOT_NAME")
    await message.answer(f"Ссылка на бота - https://t.me/{bot_name}")
